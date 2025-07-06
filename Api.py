from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
import httpx
import uvicorn
from fastapi import FastAPI, HTTPException

from AiProcessing import aiProcessing
from RegexProcessing import regexProcessing
from WebScrapper import webScrapper
from modele.ModeleCereri import *
from tools.ToolkitUtilizator import *
from tools.ToolkitOrar import *


# pool = redis.ConnectionPool(host="127.0.0.1", port=int(6379), db=int(1), password="user")
# r = redis.Redis(connection_pool=pool)
# asx = httpx.AsyncClient()


@asynccontextmanager
async def lifespan(app: FastAPI):
    #Conexiune Redis
    pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0, password="user")
    app.state.redis = redis.Redis(connection_pool=pool)

    #Client Async
    app.state.http_client = httpx.AsyncClient()

    print("Startup complet")
    yield  #aici incepe rularea API-ului

    #Inchiderea API-ului
    app.state.redis.close()
    await app.state.http_client.aclose()
    print("Shutdown complet")


app = FastAPI(
    title="Iacob's Parser",
    description="Api care face legatura intre baza de date Redis si front end, ofera acces la datele aplicatiei si diverse informatii",
    version="0.2",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/salut")
async def test_redis(request: Request):
    r = request.app.state.redis
    await r.set("test", "merge")
    return {"valoare": await r.get("test")}

@app.get("/orare-utilizator/{nume_utilizator}", response_model=list[Orar])
async def get_orare_utilizator(nume_utilizator: str, request: Request):
    r = request.app.state.redis
    orare = await obtine_orare_utilizator(r, nume_utilizator)
    return orare

@app.get("/utilizator/{nume_utilizator}")
async def get_date_utilizator(nume_utilizator: str, request: Request):
    r = request.app.state.redis
    nume, email = await obtine_date_utilizator(r, nume_utilizator)
    if not all([nume, email]):
        raise HTTPException(status_code=404, detail="Utilizator inexistent")
    return {
        "nume": nume,
        "email": email
    }

@app.post("/login")
async def login(cerere: CerereLogin, request: Request):
    print("login")
    r = request.app.state.redis
    utilizator = await descarca_utilizator_din_redis(r, cerere.nume)
    if not utilizator or not verifica_parola(cerere.parola, utilizator):
        raise HTTPException(status_code=401, detail="Date de autentificare incorecte")
    return {"mesaj": "Autentificare reușită"}

@app.post("/register")
async def register(cerere: CerereRegister, request: Request):
    r = request.app.state.redis

    #verifica daca exista deja un utilizator cu acelasi nume
    if await verificare_utilizator_duplicat(r, cerere.nume):
        raise HTTPException(status_code=400, detail="Utilizatorul există deja")

    #creaza si salveaza nou utilizator
    if all([cerere.nume,cerere.parola,cerere.email]):
        print(cerere.nume)
        utilizator = creeaza_utilizator(cerere.nume, cerere.parola, cerere.email)
        await incarca_utilizator_in_redis(r, utilizator)
    else:
        raise HTTPException(status_code=400, detail="Nu au fost introduse date pentru inregistrare")

    return {"mesaj": "Utilizator înregistrat cu succes"}


@app.post("/incarca-orar")
async def incarca_orar(orar: Orar, request: Request):
    print(orar.nume_utilizator)
    r = request.app.state.redis
    await incarca_orar_in_redis(r, orar)
    return {"mesaj": "Orarul a fost încărcat cu succes în Redis"}


@app.post("/cache-orar")
async def cache_orar(orar: Orar, request: Request):
    r = request.app.state.redis

    #verificam cache-ul actual
    exista = await verificare_orar_cache(r, orar.procesare, orar.url)
    if exista:
        return {"mesaj": "Orarul există deja în cache"}

    await incarca_orar_in_cache(r, orar)
    return {"mesaj": "Orarul a fost adăugat în cache"}


@app.post("/proceseaza-orar")
async def proceseaza_orar(cerere: CerereProcesare, request: Request) -> Orar:
    r = request.app.state.redis
    if await verificare_orar_cache(r, cerere.procesare, cerere.url):
        orar = await descarca_orar_din_cache(r, cerere.procesare, cerere.url)
        if orar is not None:
            orar.nume_utilizator = cerere.nume_utilizator
            print(orar.nume_utilizator)
            return orar
    try:
        body_list = webScrapper(cerere.url)
        if cerere.procesare == Procesare.AI:
            orar = await aiProcessing(body_list, cerere.url, cerere.nume_utilizator)
        elif cerere.procesare == Procesare.REGEX:
            orar = regexProcessing(body_list, cerere.url, cerere.nume_utilizator)
        else:
            raise HTTPException(status_code=400, detail="Procesare invalidă")
        await incarca_orar_in_cache(r, orar)
        return orar
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.delete("/clear-cache")
async def clear_cache(request: Request):
    r = request.app.state.redis
    #cauta toate cheile orarelor din cache
    chei = await r.keys("orarCache:*")
    if chei:
        await r.delete(*chei)
        return {"mesaj": f"S-au șters {len(chei)} intrări din cache."}
    return {"mesaj": "Cache-ul era deja gol."}

@app.delete("/orar/sterge")
async def sterge_orar(cerere: CerereStergereOrar, request: Request):
    r = request.app.state.redis
    cheie = f"orar:{cerere.nume_utilizator}:{cerere.procesare}:{cerere.url}"
    rezultat = await r.delete(cheie)
    if rezultat == 0:
        raise HTTPException(status_code=404, detail="Orar inexistent")
    return {"mesaj": "Orar șters cu succes"}

@app.delete("/utilizatori/sterge")
async def sterge_utilizator(
    nume: str,
    request: Request
):
    r = request.app.state.redis
    rezultat = await r.delete(f"user:{nume}")
    if rezultat == 0:
        raise HTTPException(status_code=404, detail="Utilizator inexistent")
    return {"mesaj": "Utilizator șters cu succes"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5050)
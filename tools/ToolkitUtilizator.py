import bcrypt
from modele.ModeleUtilizator import *
from typing import Union
import redis.asyncio as redis

def creeaza_utilizator(nume: str, parola_clara: str, email: str) -> Utilizator:
    salt = bcrypt.gensalt()
    parola_hash = bcrypt.hashpw(parola_clara.encode('utf-8'), salt)
    return Utilizator(nume=nume, parola=parola_hash.decode('utf-8'), email=email)

def verifica_parola(parola_introdusa: str, item: Union[Utilizator, str]) -> bool:
    if isinstance(item, Utilizator):
        parola_hash = item.parola
    else:
        parola_hash = item

    return bcrypt.checkpw(parola_introdusa.encode('utf-8'), parola_hash.encode('utf-8'))

async def incarca_utilizator_in_redis(r: redis.Redis, utilizator: Utilizator) -> None:
    await r.set(f"user:{utilizator.nume}", utilizator.model_dump_json())

async def descarca_utilizator_din_redis(r: redis.Redis, nume: str) -> Utilizator | None:
    data = await r.get(f"user:{nume}")
    if data is None:
        return None
    return Utilizator.model_validate_json(data)

async def verificare_utilizator_duplicat(r: redis.Redis, nume: str) -> bool:
    return await r.exists(f"user:{nume}") > 0

async def obtine_date_utilizator(r: redis.Redis, nume: str) -> bool:
    data = await r.get(f"user:{nume}")
    if data is None:
        return None
    utilizator = Utilizator.model_validate_json(data)
    return utilizator.nume, utilizator.email


if __name__ == "__main__":
    creeaza_utilizator("Gelu", "user", "andrei_delcea@yahoo.com")
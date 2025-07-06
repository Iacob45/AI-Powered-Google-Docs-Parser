from modele.ModeleActivitati import *
import redis.asyncio as redis


async def incarca_orar_in_redis(r: redis.Redis, orar: Orar) -> None:
    await r.set(f"orar:{orar.nume_utilizator}:{orar.procesare}:{orar.url}", orar.model_dump_json())

async def obtine_orare_utilizator(r: redis.Redis, nume_utilizator: str) -> list[Orar]:
    model = f"orar:{nume_utilizator}:*"
    cursor = 0
    orare = []

    while True:
        cursor, chei = await r.scan(cursor=cursor, match=model, count=100)
        if not chei:
            break
        for cheie in chei:
            data = await r.get(cheie)
            if data:
                try:
                    orar = Orar.model_validate_json(data)
                    orare.append(orar)
                except Exception as e:
                    print(f"Eroare la parsarea orarului de la cheia {cheie}: {e}")
        if cursor == 0:
            break

    return orare

async def incarca_orar_in_cache(r: redis.Redis, orar: Orar) -> None:
    await r.set(f"orarCache:{orar.procesare}:{orar.url}", orar.model_dump_json(), ex=86400)

async def descarca_orar_din_cache(r: redis.Redis, procesare: Procesare, url: str) -> Orar:
    data = await r.get(f"orarCache:{procesare}:{url}")
    if data is None:
        return None
    return Orar.model_validate_json(data)

async def verificare_orar_cache(r: redis.Redis, procesare: Procesare, url: str) -> bool:
    data = await r.get(f"orarCache:{procesare}:{url}")
    return data is not None

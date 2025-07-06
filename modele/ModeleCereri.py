from pydantic import BaseModel, EmailStr

from modele.ModeleActivitati import Procesare


class CerereProcesare(BaseModel):
    url: str
    procesare: Procesare
    nume_utilizator: str

class CerereLogin(BaseModel):
    nume: str
    parola: str

class CerereRegister(BaseModel):
    nume: str
    parola: str
    email: EmailStr

class CerereStergereOrar(BaseModel):
    nume_utilizator: str
    procesare: Procesare
    url: str
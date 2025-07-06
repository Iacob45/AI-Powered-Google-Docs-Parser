from pydantic import BaseModel, Field, EmailStr

class Utilizator(BaseModel):
    nume: str = Field(description="Username-ul utilizatorului")
    parola: str = Field(description="Parola hashata a utilizatorului")
    email: EmailStr = Field(description="Adresa de email a utilizatorului")
from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel, Field
from enum import Enum

class Zile(Enum):
    """Zilele saptamanii"""
    LUNI = "Luni"
    MARTI = "Marți"
    MIERCURI = "Miercuri"
    JOI = "Joi"
    VINERI = "Vineri"
    SAMBATA = "Sâmbătă"
    DUMINICA = "Duminică"

class Categorie(Enum):
    """Categoria activitatii"""
    CURS = "Curs"
    SEMINAR = "Seminar"
    LABORATOR = "Laborator"
    PROIECT = "Proiect"

class Paritate(Enum):
    """Categoria activitatii"""
    PAR = "Par"
    IMPAR = "Impar"
    AMBELE = "Ambele"

class Activitate(BaseModel):
    """Structura unei activitati"""
    id: int = Field(description="Id-ul activitatii, incepe de la 0 si se incrementeaza")
    nume: str = Field(description="Numele materiei. Exista materii cu nume mai lungi, dar si cu nume scurte,"
                                  " ex: Programarea Calculatoarelor și Limbaje de Programare 2 (curs), SEP,"
                                  " ASC, EIM, IM, G3D. De asemenea, materiile pot fi impartite"
                                  " si prin | sau || daca sunt mai multe intr-o singura celula, caz in care acestea se"
                                  " desfasoara in paralel si sunt in general optionale.")
    profesor: str = Field(description="Profesorul care se ocupa de activitate, numele lui incepe"
                                      " cu prefixele Prof., sau Profesor,"
                                      " sau Prof, prefixele nu vor fii pastrate la nume,"
                                      " profesorul poate lipsi din celula, caz in care pui -")
    sala: str = Field(description="Sala in care se desfasoara activitatea, de forma B303, sau A01,"
                                  " sau Sala Orange, sau B208a. Apare ori in celula activitatii, ori in dreapta"
                                  " celulei, ori deloc, caz in care se completeaza cu -")
    zi: Zile = Field(description="Ziua saptamanii in care se desfasoara activitatea, apare la inceputul"
                                            " fiecarui rand de tabel")
    interval: str = Field(description="Intervalul orar in care se desfasoara activitatea, se ia ora de start de la"
                                      " inceputul randului de tabel si se aduna numarul de randuri ale celulei")
    durata: int = Field(description="Durata activitatii, trebuie sa se potriveasca cu intervalul orar")
    grupe: List[str] = Field(description="Grupele care participă la activitate, apar in primul rand de tabel,"
                                         " deasupra celulelor destinate. Sunt de forma 441Da, 423Bb.")
    anul: int = Field(description="Anul de studiu, se extrage din numele uneia dintre grupele"
                                             " care participa la activitate. A doua cifra este chiar anul de studiu."
                                             " e.g. din 432Ab se extrage anul egal cu 3")
    categorie: Categorie = Field(description="Categoria activitatii (curs,seminar,laborator sau proiect,"
                                                        " prescurtate uneori (c),(s),(l),(p))")
    paritate: Paritate = Field(description="Paritatea activitatii (par sau impa, sau ambele)."
                                                      " Daca in continutul celulei apare un /, atunci ce este la stanga"
                                                      " de / este impar, iar ce este la dreapta este par. Altfel,"
                                                      " in lipsa unui / ca si paritate avem Ambele")

class Procesare(Enum):
    """Tipul de procesare"""
    AI = "AI"
    REGEX = "Regex"

class Orar(BaseModel):
    "Contine lista de activitati"
    url: str = Field(description="URL sursa al orarului")
    nume_utilizator: str = Field(description="Identificatorul unic al utilizatorului, numele")
    procesare: Procesare = Field(description="Motorul de procesare folosit")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Momentul când orarul a fost salvat")
    activitati: List[Activitate] = Field(description="Lista de activitati inlantuite")
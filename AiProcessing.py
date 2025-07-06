from bs4 import ResultSet, Tag
from openai import AsyncOpenAI
import instructor
from dotenv import load_dotenv
from WebScrapper import webScrapper
from modele.ModeleActivitati import *

async def aiProcessing(body_list: ResultSet[Tag], url: str, nume_utilizator: str):
    print("\nStart AiProcessing")
    #incarcare cheie API
    load_dotenv()

    start = 3
    batch_size = 10
    lista_raspunsuri = []
    # creere client folosind instructor si OpenAI
    client = instructor.from_openai(AsyncOpenAI())

    while start < len(body_list):
        print("Suntem la randul: ",start)
        #obtinere continut html
        batch = [body_list[1]] + body_list[start : start + batch_size]
        #html_content = batch
        html_content = ''.join(str(row) for row in batch)

        #Prompt catre OpenAI, se foloseste o iesire structurata dupa model pydantic
        response = await client.chat.completions.create(
            model='gpt-4o',
            max_retries=10,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Următorul conținut HTML reprezintă mai multe rânduri de orar universitar:
        
                    {html_content}
        
                    Extrage TOATE activitățile individuale din acest HTML. Atenție:
                    - Unele celule pot conține MAI MULTE activități (ex: "CD(l) / AP(s)"). Fiecare activitate trebuie tratată separat.
                    - Exista materii cu nume scurte, prescurtate, ex: SEP (l), ASC (l), EIM (l), IM (l), G3D (l)
                    - Tipurile pot fi curs (c), laborator (l), seminar (s), proiect (p) – dar pot apărea fără mențiune explicită.
                    - Dacă în text apare `/`, este foarte probabil să fie activități separate cu paritate diferită. Extrage-le separat.
                    - Daca o activitate are numele lipsa, de ex: '-', atunci nu o adauga in lista
                    - Completează toate câmpurile modelului Activitate:
                      - `nume`: numele materiei, fără simboluri auxiliare
                      - `profesor`: dacă există, fără prefixe (Prof., Profesor etc.)
                      - `sala`: dacă nu e specificată, pune "-"
                      - `zi`, `interval`, `durata`, `grupe`, `anul`, `categorie`, `paritate`
        
                    Returnează o LISTĂ JSON completă de obiecte de tip `Activitate`, câte unul pentru fiecare activitate (inclusiv curs, laborator, seminar si proiect).
                    Exemplu de output corect:
                    [Activitate(id=0, nume='SEP', profesor='-', sala='-', zi=<Zile.LUNI: 'Luni'>, interval='09-11', durata=2, grupe=['441Ba', '441Bb'], anul=4, categorie=<Categorie.LABORATOR: 'Laborator'>, paritate=<Paritate.IMPAR: 'Impar'>), Activitate(id=1, nume='ASC', profesor='-', sala='-', zi=<Zile.LUNI: 'Luni'>, interval='09-11', durata=2, grupe=['441Ba', '441Bb'], anul=4, categorie=<Categorie.LABORATOR: 'Laborator'>, paritate=<Paritate.PAR: 'Par'>)]
                    """
                }
            ],
            response_model=List[Activitate]
        )
        lista_raspunsuri.extend(response)
        start += batch_size

    #Afisare raspuns
    id_actual = 0
    for i in lista_raspunsuri:
        i.id=id_actual
        id_actual += 1
        print(i)
    print("Lungime lista activitati: ", len(lista_raspunsuri))
    orar = Orar(url=url, nume_utilizator=nume_utilizator, procesare="AI", activitati=lista_raspunsuri)
    return orar

if __name__ == "__main__":
    url = "https://docs.google.com/spreadsheets/d/1VZv4gzrwjshWxZLtmjD1xzSL9sTPjliNeu17SJ0DEuA/edit?pli=1&gid=814253745#gid=814253745"
    nume_utilizator = "Iacob"
    orar = aiProcessing(webScrapper(url), url, nume_utilizator)
    print(orar)
from bs4 import ResultSet, Tag
from WebScrapper import webScrapper
from modele.ModeleRegex import *
from modele.ModeleActivitati import *

grupe_header = []
index_rand_grupe = -1

def verifica_model(text, *args):
    bool_list = []
    for intrare in args:
        if type(intrare) == list:
            for model in intrare:
                if model.search(text):
                    bool_list.append(True)
                else:
                    bool_list.append(False)
        else:
            if intrare.search(text):
                bool_list.append(True)
            else:
                bool_list.append(False)
    return any(bool_list)

def cauta_sali(celula, index, *args):
    global grupe_header
    if verifica_model(celula.text, modele_sali) and grupe_header[index] == "N/A":
        grupe_header[index] = "sala"
    return celula.text

def afla_interval(ora_start, celula):
    if ora_start:
        ora_start = int(ora_start)
        durata = int(celula.get('rowspan', '1'))
        interval = f"{ora_start:02}" + '-' + f"{ora_start + durata:02}"
        return interval, durata
    else:
        return '-', '-'

def afla_grupe(celula, index):
    global grupe_header
    grupe = []
    for i in range(index,index+int(celula.get('colspan', '1'))):
        if verifica_model(grupe_header[i], model_grupe):
            grupe.append(grupe_header[i])
    if grupe != []:
        anul = grupe[0][1]
        return grupe, anul
    return ['-'], '-'

def cauta_sala(text):
    for model in modele_sala_continut:
        match = model.search(text)
        if match:
            sala = match.group(1)
            return sala

    return '-'

def cauta_profesor(text):
    match = model_profesor.search(text)
    if match:
        profesor = match.group(2)
        return profesor

    return '-'

def imparte_pe_paritate(text):
    split = text.split('/')
    elemente = len(split)
    lista = []
    if elemente == 1:
        lista.append({"text": text, "paritate": "Ambele"})
    else:
        if verifica_model(split[0].strip(), model_activitate):
            lista.append({"text": split[0].strip(), "paritate": "Impar"})
        if verifica_model(split[elemente-1].strip(), model_activitate):
            lista.append({"text": split[elemente-1].strip(), "paritate": "Par"})

    return lista

def imparte_mai_multe(text):
    split = text.split('|')
    elemente = len(split)
    lista = []
    if elemente == 1:
        split2 = re.split(model_optional, text.strip())
        for element2 in split2:
            if verifica_model(element2, model_activitate):
                lista.append(element2.strip())
    else:
        for element in split:
            if verifica_model(element, model_activitate):
                lista.append(element.strip())
    return lista

def cauta_categorie(text):
    if verifica_model(text, modele_categorie_curs):
        return "Curs"
    elif verifica_model(text, modele_categorie_seminar):
        return "Seminar"
    elif verifica_model(text, modele_categorie_laborator):
        return "Laborator"
    elif verifica_model(text, modele_categorie_proiect):
        return "Proiect"
    else:
        return "Curs"

def curata_dupa_model(text, *args) -> str:
    for intrare in args:
        if type(intrare) == list:
            for model in intrare:
                text_curatat = model.sub('', text).strip()
                text = text_curatat if text_curatat else text
        else:
            text_curatat = intrare.sub('', text).strip()
            text = text_curatat if text_curatat else text
    return text

def curatare_nume(text) -> str:
    textvechi=text
    #sterge numele profesorului, salii, tipul de activitate, dupa model
    text = curata_dupa_model(text, model_profesor, modele_sala_continut, modele_categorie_proiect,
                             modele_categorie_seminar, modele_categorie_laborator, modele_categorie_curs, modele_caractere)
    return text


def cauta_activitati(celula, index, *args):
    global grupe_header
    lista_activitati = args[0]
    context = args[1]
    contor_activitati = args[1]["contor_activitati"]
    id_actual = args[1]["id_actual"]
    zi = args[1]["zi"]
    ora_start = args[1]["ora_start"]
    text = celula.text.strip()
    continut = '-'
    profesor = '-'
    sala = '-'
    interval = '-'
    durata = '-'
    grupe = ['-']
    anul = '-'
    categorie = 'Curs'
    paritate = 'Ambele'
    if (verifica_model(text, modele_zile)):
        if verifica_model(text, modele_zile[0]):
            zi = "Luni"
        if verifica_model(text, modele_zile[1]):
            zi = "Marți"
        if verifica_model(text, modele_zile[2]):
            zi = "Miercuri"
        if verifica_model(text, modele_zile[3]):
            zi = "Joi"
        if verifica_model(text, modele_zile[4]):
            zi = "Vineri"
        if verifica_model(text, modele_zile[5]):
            zi = "Sâmbătă"
        if verifica_model(text, modele_zile[6]):
            zi = "Duminică"
    elif (verifica_model(text, model_ore)):
        ora_start = text.split('-')[0].strip()
    elif (verifica_model(text, modele_sali) and ora_start != '-'):
        sala = text
        for i in range(contor_activitati):
            if lista_activitati[-1-i].sala == '-':
                lista_activitati[-1-i].sala = sala
        contor_activitati = 0
    elif (not verifica_model(text, model_grupe)
          and verifica_model(text, model_activitate)
          and not verifica_model(grupe_header[index], model_sala)
          and ora_start != '-'):
        interval, durata = afla_interval(ora_start, celula)
        grupe, anul = afla_grupe(celula, index)
        if grupe != ['-']:
            continut = imparte_pe_paritate(text)
            print(text)
            for activitati in continut:
                paritate = activitati["paritate"]
                nNume = activitati["text"]
                continut2 = imparte_mai_multe(nNume)
                for activitate in continut2:
                    nume = activitate
                    contor_activitati += 1
                    id_actual = id_actual + 1
                    sala = cauta_sala(nume)
                    categorie = cauta_categorie(nume)
                    profesor = cauta_profesor(nume)
                    nume = curatare_nume(nume)
                    lista_activitati.append(Activitate(
                        id = id_actual,
                        nume = nume,
                        profesor = profesor,
                        sala = sala,
                        zi = zi,
                        interval = interval,
                        durata = durata,
                        grupe = grupe,
                        anul = anul,
                        categorie = categorie,
                        paritate = paritate,
                    ))
    if grupe_header[index] == "sala":
        contor_activitati = 0
    context["id_actual"] = id_actual
    context["contor_activitati"] = contor_activitati
    context["zi"] = zi
    context["ora_start"] = ora_start
    return lista_activitati

def parcurgere_cu_index(body_list, functie, *args):
    global index_rand_grupe
    global grupe_header
    return_list = []
    final_rand = 0
    contor_coloana = [0] * len(grupe_header)
    try:
        for rand in body_list[index_rand_grupe + 1:]:
            if args:
                args[1]["ora_start"] = '-'
                args[1]["contor_activitati"] = 0
            index = 0
            for celula in rand:
                while contor_coloana[index] > 0:
                    contor_coloana[index] -= 1
                    if index == len(contor_coloana)-1:
                        final_rand = 1
                        break
                    index += 1
                if final_rand:
                    final_rand = 0
                    break
                return_list.append(functie(celula, index, *args))
                colspan = int(celula.get('colspan', '1'))
                rowspan = int(celula.get('rowspan', '1'))
                contor_coloana[index:index + colspan] = [rowspan - 1] * colspan
                index += colspan
    except Exception as e:
        print("Problema la parcurgerea cu index", e)

    return return_list

def regexProcessing(body_list: ResultSet[Tag], url: str, nume_utilizator: str):
    global index_rand_grupe
    global grupe_header
    print("\nStart RegexProcessing")



    #cautare grupe
    index_rand = 0

    for rand in body_list:
        grupe_header = []
        grupe_adaugate = 0
        for celula in rand:
            if verifica_model(celula.text, model_grupe):
                grupe_header.append(celula.text.strip())
                grupe_adaugate += 1
            #verificare coloana de sali
            elif verifica_model(celula.text, model_sala,):
                grupe_header.append("sala")
            else:
                grupe_header.append("N/A")
        if grupe_adaugate > 4:
            index_rand_grupe = index_rand
            break
        index_rand += 1

    #verificare daca au fost gasite grupe
    if grupe_header == []:
        grupe_header = ["N/A"] * len(body_list[1])

    #acest contor tine cont cate randuri mai este ocupata o coloana
    contor_coloana = [0] * len(grupe_header)

    #verificare suplimentara coloane de sali
    parcurgere_cu_index(body_list, cauta_sali)

    print("Update grupe cu coloane sali:", grupe_header)


    #cautare activitate
    lista_activitati = []
    context = {"id_actual": -1,
               "contor_activitati": 0,
               "ora_start": "-",
               "zi": "-"}
    parcurgere_cu_index(body_list, cauta_activitati, lista_activitati, context)
    print("Lungime lista activitati: ", len(lista_activitati))


    orar = Orar(url=url, nume_utilizator=nume_utilizator, procesare="Regex", activitati=lista_activitati)
    return orar

if __name__ == "__main__":
    url = "https://docs.google.com/spreadsheets/d/1VZv4gzrwjshWxZLtmjD1xzSL9sTPjliNeu17SJ0DEuA/edit?pli=1&gid=814253745#gid=814253745"
    url2 = "https://docs.google.com/spreadsheets/d/15sr4wJK_VMuQDEYggxj6EbeRZU2-u4fuaWPaV2id05Q/edit?gid=814253745#gid=814253745"
    url3 = "https://docs.google.com/spreadsheets/u/0/d/1RBZOdt2100S9NBBeA81unABfkBxa_2TEZh4brfXyBQE/htmlview#"
    url4 = "https://docs.google.com/spreadsheets/d/1VZv4gzrwjshWxZLtmjD1xzSL9sTPjliNeu17SJ0DEuA/edit?pli=1&gid=1088080427#gid=1088080427"
    url5 = "https://docs.google.com/spreadsheets/d/1VZv4gzrwjshWxZLtmjD1xzSL9sTPjliNeu17SJ0DEuA/edit?pli=1&gid=1578046571#gid=1578046571"
    nume_utilizator = "Iacob"
    orar = regexProcessing(webScrapper(url5), url5, nume_utilizator)
    print(orar)
import re

#Modele regex precompilate
model_grupe = re.compile("^[ ]{0,2}[0-9]{3}[A-Za-z][A-Za-z]{0,1}[ ]{0,2}$")

modele_zile = []
modele_zile.append(re.compile("^[ ]{0,2}[Ll][Uu][Nn][Ii][ ]{0,2}$"))
modele_zile.append(re.compile("^[ ]{0,2}[Mm][Aa][Rr][TtȚț][Ii][ ]{0,2}$"))
modele_zile.append(re.compile("^[ ]{0,2}[Mm][Ii][Ee][Rr][Cc][Uu][Rr][Ii][ ]{0,2}$"))
modele_zile.append(re.compile("^[ ]{0,2}[Jj][Oo][Ii][ ]{0,2}$"))
modele_zile.append(re.compile("^[ ]{0,2}[Vv][Ii][Nn][Ee][Rr][Ii][ ]{0,2}$"))
modele_zile.append(re.compile("^[ ]{0,2}[Ss][AaÂâ][Mm][Bb][AaĂă][Tt][Ăă][ ]{0,2}$"))
modele_zile.append(re.compile("^[ ]{0,2}[Dd][Uu][Mm][Ii][Nn][Ii][Cc][AaĂă][ ]{0,2}$"))

model_sala = re.compile("^[ ]{0,2}[Ss][Aa][Ll][AaĂă][ ]{0,2}$")

modele_sali = []
modele_sali.append(re.compile("^[ ]{0,2}[BbAa][0-9]{1,4}[A-Za-z]{0,1}[ ]{0,2}$"))
modele_sali.append(re.compile("^[ ]{0,2}[Ss][Aa][Ll][AaĂă]"))

modele_sala_continut = []
modele_sala_continut.append(re.compile("([BbAa][0-9]{1,4}[A-Za-z]{0,1})"))
modele_sala_continut.append(re.compile(r"\b[Ss][Aa][Ll][AaĂă][ ]{0,2}\w+"))

model_activitate = re.compile("[A-Za-z]{2,}")

model_ore = re.compile("^[ ]{0,2}[0-9]{0,1}[0-9][-][0-9][0-9]{0,1}[ ]{0,2}$")

modele_categorie_curs = []
modele_categorie_curs.append(re.compile(r"\(+[ ]{0,2}[Cc][Uu][Rr][Ss][ ]{0,2}\)+"))
modele_categorie_curs.append(re.compile(r"\(+[ ]{0,2}[Ll][Ee][Cc][Tt][Uu][Rr][Ee][ ]{0,2}\)+"))
modele_categorie_curs.append(re.compile(r"\(+[ ]{0,2}[Cc][ ]{0,2}\)+"))
modele_categorie_seminar = []
modele_categorie_seminar.append(re.compile(r"\(+[ ]{0,2}[Ss][Ee][Mm][Ii][Nn][Aa][Rr][ ]{0,2}\)+"))
modele_categorie_seminar.append(re.compile(r"\(+[ ]{0,2}[Ss][ ]{0,2}\)+"))
modele_categorie_laborator = []
modele_categorie_laborator.append(re.compile(r"\(+[ ]{0,2}[Ll][Aa][Bb][Oo][Rr][Aa][Tt][Oo][Rr][Yy][ ]{0,2}\)+"))
modele_categorie_laborator.append(re.compile(r"\(+[ ]{0,2}[Ll][Aa][Bb][Oo][Rr][Aa][Tt][Oo][Rr][ ]{0,2}\)+"))
modele_categorie_laborator.append(re.compile(r"\(+[ ]{0,2}[Ll][ ]{0,2}\)"))
modele_categorie_proiect = []
modele_categorie_proiect.append(re.compile(r"\(+[ ]{0,2}[Pp][Rr][Oo][Jj][Ee][Cc][Tt][ ]{0,2}\)+"))
modele_categorie_proiect.append(re.compile(r"\(+[ ]{0,2}[Pp][Rr][Oo][Ii][Ee][Cc][Tt][ ]{0,2}\)+"))
modele_categorie_proiect.append(re.compile(r"\(+[ ]{0,2}[Pp][ ]{0,2}\)+"))

model_optional = re.compile(r"(?=\s*[Oo]([Pp][Tt][.\s]*\d+|[1-9]\.*(?=\W|$)))")


model_profesor = re.compile(r"(Prof\.?|Profesor|Professor)\s?([A-Za-zĂăÂâÎîȘșȚț .\-]+)", re.IGNORECASE)

modele_caractere = []
modele_caractere.append(re.compile(r"^[^a-zA-Z0-9ĂăÂâÎîȘșȚț]+"))
modele_caractere.append(re.compile(r"[^a-zA-Z0-9ĂăÂâÎîȘșȚț]+$"))

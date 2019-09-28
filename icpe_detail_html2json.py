import sys
import json
import re

from bs4 import BeautifulSoup


xml = open(sys.argv[1])
icpe = BeautifulSoup(xml.read(), 'lxml')

data = {'id': '', 'nom':'', 'details': [], 'documents': [], 'adresse': ''}

contenu = icpe.find(id='contenu')

# extraction du nom de l'établissement
nom = ''
for s in contenu.find('h2').strings:
    nom = nom + s
data['nom'] = nom.replace('Nom (1) : ','')

# extraction des informations sur l'établissement (texte non structuré)
infos = contenu.find(class_='contenuArticle')
state = 0
for i in infos.strings:
    txt = i.replace('\n','').split(':')
    if state == 1:
        if len(txt) == 1:
            data["adresse"] = (data["adresse"]+"  "+txt[0]).strip()
        else:
            state = 2
    if state == 0 and txt[0] == "Adresse d'exploitation ":
        state = 1
    if state == 2:
        if len(txt)>1 and txt[1] == '-':
            txt[1] = ''
        if txt[0] == 'Activité principale ':
            data['activite_principale'] = txt[1].strip()
        if txt[0] == "Etat d'activité ":
            data['etat_activite'] = txt[1].strip()
        if txt[0] == "Service inspection ":
            data['service_inspection'] = txt[1].strip()
        if txt[0] == "Numéro inspection ":
            data['id'] = txt[1].strip()
        if txt[0] == "Dernière inspection ":
            data['date_inspection'] = re.sub(r"(..)/(..)/(....)", r"\3-\2-\1", txt[1].strip())
        if txt[0] == "Statut Seveso ":
            data['statut_seveso'] = txt[1].strip()
        if txt[0] == "Priorité nationale ":
            data['priorite_nationale'] = txt[1].strip()
        if txt[0] == 'IED-MTD ':
            data['ied_mtd'] = txt[1].strip()
        if txt[0] == ' ':
            data['regime'] = txt[1].strip()

# tableau de situation administrative
infos = contenu.find(summary="liste des résultats")
if infos:
    for info in infos.find_all('tr'):
        col = info.find_all('td')
        if len(col)>0:
            j = {'rubrique': col[0].string,
                'ali': col[1].string,
                'date_autorisation': col[2].string.strip(),
                'etat_activite': col[3].string.strip(),
                'regime_autorise': col[4].string.strip(),
                'activite': col[5].string.strip(),
                'volume': col[6].string.replace('-','').replace(',','.').strip(),
                'unite': col[7].string.strip()
                }
            # conversion date en ISO
            j['date_autorisation'] = re.sub(r"(..)/(..)/(....)",
                                            r"\3-\2-\1", j['date_autorisation'])
            # conversion volume en numérique
            try:
                j['volume'] = float(j['volume'])
            except:
                pass
            data['details'].append(j)

# table de liste des documents publics
docs = contenu.find(summary="liste des documents disponibles")
if docs:
    for doc in docs.find_all('tr'):
        col = doc.find_all('td')
        if len(col) > 0:
            j = {'date': col[0].string,
                'type': col[1].string,
                'description': col[2].string,
                'url': col[2].find('a').get('href')
                }
            data['documents'].append(j)

# liens vers autres bases (répertoire des émissions, base des sols pollués)
data['irep'] = False
data['basol'] = False
for link in contenu.find_all('a'):
    if link.get('href'):
        if 'www.pollutionsindustrielles.ecologie.gouv.fr' in link.get('href'):
            data['irep'] = True
        if 'basol.developpement-durable.gouv.fr' in link.get('href'):
            data['basol'] = True

print(json.dumps(data))

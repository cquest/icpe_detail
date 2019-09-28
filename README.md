# icpe_detail

Scripts d'extraction des données détaillées sur les ICPE disponible sur le site http://www.installationsclassees.developpement-durable.gouv.fr/

Les données traitées sont téléchargeables sur http://data.cquest.org/icpe/

## icpe_detail.sh

- récupère la liste des ICPE au format CSV
- télécharge les pages HTML contenant les informations détaillées
- appelle icpe_detail_html2json.py

## icpe_detail_html2json.py

- parse le contenu d'un fichier HTML
- extrait les informations et génère un json en sortie


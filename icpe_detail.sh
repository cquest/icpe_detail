# récupération des détails des fiches
rm icpe_tmp.json
curl http://www.installationsclassees.developpement-durable.gouv.fr/ic_export.php -H 'User-agent: Mozilla/5.0' > icpe_last.csv
for ID in $(sed 's/;.*//;s/"//g' icpe_last.csv | tail -n +2)
do
    echo $ID
    ID1=$(echo $ID | sed 's/\..*$//')
    ID2=$(echo $ID | sed 's/^.*\.//')
    mkdir -p data/$ID1
    wget -q -nc "http://www.installationsclassees.developpement-durable.gouv.fr/ficheEtablissement.php?champEtablBase=$ID1&champEtablNumero=$ID2" -O data/$ID1/$ID.html
    python icpe_detail_html2json.py data/$ID1/$ID.html | jq -S -c . >> icpe_tmp.json
done

jq -s . icpe_tmp.json | gzip -9 > icpe_detail.json.gz

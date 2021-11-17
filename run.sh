#!/bin/bash

# Upload Dashboard to Grafana
grafanaDashboard=$(<./grafana/grafana_dashboard.json)
curl -X POST http://admin:admin@localhost:3000/api/dashboards/db -H 'Accept: application/json' -H 'Content-Type: application/json' -d "{\"dashboard\":$grafanaDashboard}"

echo "Dashboard created"

# Upload Datasource to Grafana
grafanaDatasource=$(<./grafana/grafana_datasource.json)
curl -X POST http://admin:admin@localhost:3000/api/datasources -H 'Accept: application/json' -H 'Content-Type: application/json' -d "$grafanaDatasource"

echo "Datasource created"
echo "======="

while IFS=, read -r name email
do
    emaill=`echo $email | sed 's/\\r//g'`
    #echo $emaill
    #echo "{\"name\": \"$name\",\"email\": \"$email\"}"
    JSON_STRING='{"name":"'"$name"'","email":"'"$emaill"'"}'
    #echo $JSON_STRING

    curl --request POST \
    --url http://localhost:8000/users \
    --header 'content-type: application/json' \
    --data $JSON_STRING

done < <(tail -n +2 feed.csv)
#!/bin/bash

curl -i -X POST -H "Content-Type: application/json" \
    2>/dev/null \
    -d '{"username":"a","password":"b"}' \
    http://localhost:5000/api/users/add >/dev/null

TOKEN_FULL=$(curl -u a:b -i -X GET http://localhost:5000/api/token)
TOKEN=$(echo ${TOKEN_FULL} \
    2>/dev/null \
    | grep token \
    | tail -n 1 \
    | cut -d ':' -f 2 \
    | sed -e 's,",,g')

echo $TOKEN
curl -u $TOKEN:unused -i -X GET http://localhost:5000/api/secret

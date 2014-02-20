#!/bin/bash

rm app/db.sqlite
python2.7 -c "from app import db; db.create_all()"

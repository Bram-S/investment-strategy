#!/bin/bash

python3 updateAll.py

git add .

git commit -am "updated data"

git push

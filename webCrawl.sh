#!/bin/bash

cd $2
git init
wget --wait=2 --limit-rate=20K -r -p -U Mozilla --reject-regex "(.*)\?(.*)" $1
git add .
git commit -m"Crawled website"


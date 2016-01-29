#!/bin/bash

echo "--Creating a new tmp branch..."
git checkout -b tian_clean_master_tmp
echo "--Removing current master..."
git branch -D master
echo "--Fetching a new master..."
git fetch origin master
echo "--Checking out, reset, and pull..."
git checkout master
git reset --hard origin/master
git pull --ff-only origin master
echo "--Removing tmp branch..."
git branch -D tian_clean_master_tmp
echo
echo "--Done"
echo

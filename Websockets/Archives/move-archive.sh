#!/usr/bin/bash

current_date=$(date +'%m-%d-%Y')

cp "../live-btc-data.csv" "${current_date}-btc.csv"

cp "../pattern-data.csv" "${current_date}-pattern-data.csv"

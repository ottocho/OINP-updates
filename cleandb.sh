#!/bin/bash

export TZ='America/New_York'
cd /home/otto_cho/OINP-updates/
find db -mtime +10 -exec rm -rf {} \;


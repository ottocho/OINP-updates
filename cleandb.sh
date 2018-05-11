#!/bin/bash

export TZ='America/Toronto'
cd /home/otto_cho/onipu/
find db -mtime +10 -exec rm -rf {} \;


#!/usr/bin/env bash
#export PATH=/usr/local/mongodb/bin:$PATH && sudo mongod &
python3 crawler.py &
python3 spider.py &

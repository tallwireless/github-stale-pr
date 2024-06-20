from python:3.12-alpine

workdir /usr/src/app

copy reqs-prod.txt ./
run pip install --no-cache-dir -r reqs-prod.txt

copy . .

cmd ["python3", "./github-stale-pr.py"]

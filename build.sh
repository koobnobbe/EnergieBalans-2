#!/bin/bash
docker build -t python310_kno .
docker run --name flask_app  -p 8000:5000 python310_kno

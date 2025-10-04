#!/bin/bash

set -e

echo "Aplicando migrations..."

cd core
alembic upgrade head

cd ..

echo "Migrations aplicadas com sucesso!"
echo "________________________________"
echo "Iniciando aplicação..."

exec python3 main_server.py
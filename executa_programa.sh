#!/bin/bash

# Navega para a pasta raiz do projeto
cd "$(dirname "$0")" || exit

# Ativa o ambiente virtual, se estiver usando
# source venv/bin/activate

# Executa o script Python
python3 Source/Front/main.py

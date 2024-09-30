#!/bin/bash

# Navega para a pasta raiz do projeto
cd "$(dirname "$0")" || exit

# Nome do ambiente virtual
ENV_NAME="venv"

# Verifica se o ambiente virtual já existe
if [ ! -d "$ENV_NAME" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv "$ENV_NAME"
fi

# Ativa o ambiente virtual
source "$ENV_NAME/bin/activate"

# Instala as dependências, se necessário
pip install -r requirements.txt

# Executa o script Python
echo "Executando o script executa_programa.sh..."
./executa_programa.sh

# Verifique se a execução foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "O script executa_programa.sh foi executado com sucesso."
else
    echo "Houve um erro ao executar o script executa_programa.sh."
fi

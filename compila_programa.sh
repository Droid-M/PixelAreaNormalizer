#!/bin/bash

# Diretório onde o executável será gerado
BUILD_DIR="./build"

# Comando para compilar com cx_Freeze
BUILD_COMMAND="python Source/setup.py build"

# Verifica se o diretório de compilação existe, se não, cria
mkdir -p "$BUILD_DIR"

# Executa o comando de compilação
echo "Iniciando a compilação..."
$BUILD_COMMAND

# Verifica se a compilação foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "Compilação concluída com sucesso."
else
    echo "Erro na compilação."
fi
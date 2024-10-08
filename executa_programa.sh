#!/bin/bash

# Navega para a pasta raiz do projeto
cd "$(dirname "$0")" || exit

# Verifica se o python3-qgis está instalado
if ! dpkg -l | grep -q python3-qgis; then
    echo "O pacote python3-qgis não está instalado. Instalando agora..."
    
    # Usar gksudo ou pkexec para instalação gráfica
    if command -v gksudo &> /dev/null; then
        gksudo bash -c "apt install -y python3-qgis"
    elif command -v pkexec &> /dev/null; then
        pkexec bash -c "apt install -y python3-qgis"
    else
        echo "Nenhum método gráfico disponível para instalação."
        exit 1
    fi
else
    echo "O pacote python3-qgis já está instalado."
fi

# Define o arquivo de configuração
CONFIG_FILE="$HOME/.bashrc"  # Ou outro arquivo de configuração desejado

# Caminho a ser adicionado
EXPORT_LINE="export PYTHONPATH=/usr/share/qgis/python"

# Verifica se a linha já existe no arquivo de configuração
if ! grep -qF "$EXPORT_LINE" "$CONFIG_FILE"; then
    echo "$EXPORT_LINE" >> "$CONFIG_FILE"
    echo "Adicionado: $EXPORT_LINE"
else
    echo "A linha já existe no arquivo de configuração."
fi

# Caminho do executável gerado
EXECUTABLE="./Source/build/exe.linux-x86_64-3.11/main"

# Verifica se o executável existe e o executa, caso contrário, executa o script Python
if [[ -f "$EXECUTABLE" ]]; then
    echo "Executando o aplicativo compilado..."
    "$EXECUTABLE"
else
    echo "Executável não encontrado. Executando o script Python..."
    python3 Source/main.py
fi
import cv2
import numpy as np
import os
import argparse
import logging

def configura_logs():
    # Configurar o logging
    logging.basicConfig(
        filename='processamento_imagens.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


# Função para calcular a área por pixel
def calcular_area_por_pixel(area_km2, altura, largura):
    total_pixels = altura * largura
    area_por_pixel = area_km2 / total_pixels
    return area_por_pixel

# Função para normalizar as áreas por pixel
def normalizar_areas(areas):
    max_area = max(areas)
    return [area / max_area for area in areas]

def ler_imagem(caminho_imagem):
    if not os.path.exists(caminho_imagem):
        logging.error(f"Caminho inválido: {caminho_imagem}")
        return None
    return cv2.imread(caminho_imagem)

# Função para calcular a soma ponderada das intensidades e pelas áreas normalizadas
def soma_ponderada_intensidades(imagem, area_normalizada):
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    intensidades = np.sum(imagem_cinza)
    return intensidades * area_normalizada

def main(imagens, areas_km2):
    if not imagens:
        logging.error("Erro: Nenhuma imagem foi fornecida.")
        return {}

    if len(imagens) != len(areas_km2):
        logging.error("Erro: O número de imagens deve ser igual ao número de áreas.")
        return {}

    areas_por_pixel = []
    resultados = {}

    # Ler cada imagem, calcular as áreas por pixel e armazenar
    for i, caminho_imagem in enumerate(imagens):
        if areas_km2[i] < 0:
            logging.error(f"Erro: Área negativa fornecida para {caminho_imagem}.")
            continue
        
        imagem = ler_imagem(caminho_imagem)

        if imagem is None:
            logging.error(f"Erro ao carregar {caminho_imagem}. Verifique se o arquivo é uma imagem válida.")
            continue

        altura, largura, _ = imagem.shape
        area_por_pixel = calcular_area_por_pixel(areas_km2[i], altura, largura)
        areas_por_pixel.append(area_por_pixel)

    areas_normalizadas = []
    if not areas_por_pixel:  # Verifica se a lista está vazia
        logging.warning("Nenhuma área válida foi fornecida para normalização.")
    else:
        # Normalizar as áreas por pixel
        areas_normalizadas = normalizar_areas(areas_por_pixel)

    # Fazer a soma ponderada das intensidades de níveis de cinza para cada imagem
    for i, caminho_imagem in enumerate(imagens):
        imagem = ler_imagem(caminho_imagem)

        if imagem is None:
            continue
        
        soma_ponderada = soma_ponderada_intensidades(imagem, areas_normalizadas[i])

        # Armazenar resultados com mais informações
        resultados[caminho_imagem] = {
            'caminho_imagem': caminho_imagem,
            'soma_ponderada': soma_ponderada,
            'area_por_pixel': areas_por_pixel[i],
            'area_normalizada': areas_normalizadas[i]
        }
        
        logging.info(f"Soma ponderada para {caminho_imagem}: {soma_ponderada}")

    return resultados

if __name__ == "__main__":
    configura_logs()
    
    parser = argparse.ArgumentParser(description="Processar imagens e calcular soma ponderada das intensidades.")
    parser.add_argument('imagens', nargs='+', help='Caminhos completos das imagens a serem processadas.')
    parser.add_argument('areas_km2', nargs='+', type=float, help='Áreas estimadas em km² para cada imagem.')

    args = parser.parse_args()

    resultados = main(args.imagens, args.areas_km2)
    if resultados:
        logging.info(f"Resultados: {resultados}")
        print(resultados)
    else:
        print({})

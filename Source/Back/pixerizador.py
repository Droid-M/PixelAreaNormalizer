import cv2
import numpy as np
import os
import argparse
import logging

def configurar_logs():
    """
    Configura o sistema de logging para registrar eventos e erros em um arquivo.
    O arquivo de log será chamado 'processamento_imagens.log'.
    """
    logging.basicConfig(
        filename='processamento_imagens.log',  # Nome do arquivo onde os logs serão armazenados.
        level=logging.DEBUG,  # Define o nível de logging; DEBUG para registrar tudo.
        format='%(asctime)s - %(levelname)s - %(message)s'  # Formato das mensagens de log.
    )

# Função para calcular a área representada por cada pixel
def calcular_area_por_pixel(area_km2, altura, largura):
    """
    Calcula a área correspondente a cada pixel com base na área total em km²
    e nas dimensões da imagem.
    
    :param area_km2: Área total em quilômetros quadrados.
    :param altura: Altura da imagem em pixels.
    :param largura: Largura da imagem em pixels.
    :return: Área por pixel.
    """
    total_pixels = altura * largura  # Calcula o total de pixels na imagem.
    area_por_pixel = area_km2 / total_pixels  # Calcula a área correspondente a cada pixel.
    return area_por_pixel

# Função para normalizar as áreas por pixel em relação à maior área
def normalizar_areas(areas):
    """
    Normaliza as áreas para que a maior área se torne 1.
    
    :param areas: Lista de áreas a serem normalizadas.
    :return: Lista de áreas normalizadas.
    """
    max_area = max(areas)  # Encontra a maior área.
    return [area / max_area for area in areas]  # Normaliza cada área.

def ler_imagem(caminho_imagem):
    """
    Lê uma imagem do caminho especificado, verificando se o caminho existe.
    
    :param caminho_imagem: Caminho completo da imagem a ser lida.
    :return: A imagem lida ou None se o caminho for inválido.
    """
    if not os.path.exists(caminho_imagem):  # Verifica se o caminho existe.
        logging.error(f"Caminho inválido: {caminho_imagem}")  # Loga erro se o caminho for inválido.
        return None
    return cv2.imread(caminho_imagem)  # Lê a imagem usando OpenCV.

# Função para calcular a soma ponderada das intensidades da imagem
def soma_ponderada_intensidades(imagem_cinza, area_normalizada):
    """
    Calcula a soma ponderada das intensidades da imagem em níveis de cinza.
    
    :param imagem: A imagem a ser processada.
    :param area_normalizada: A área normalizada correspondente à imagem.
    :return: Soma ponderada das intensidades.
    """
    intensidades = np.sum(imagem_cinza)  # Calcula a soma das intensidades de pixels.
    return intensidades * area_normalizada  # Retorna a soma ponderada.

def registra_processamento(resultados, caminho_imagem, soma_ponderada=None, area_por_pixel=None, area_normalizada=None, histograma=None, erro_processamento=None):
    """
    Registra os resultados do processamento de cada imagem em uma lista.
    
    :param resultados: Lista onde os resultados serão armazenados.
    :param caminho_imagem: Caminho da imagem processada.
    :param soma_ponderada: Soma ponderada das intensidades da imagem.
    :param area_por_pixel: Área por pixel calculada.
    :param area_normalizada: Área normalizada calculada.
    :param erro_processamento: Mensagem de erro, se houver.
    """
    resultados.append({
        "erro_processamento": erro_processamento,
        "caminho_imagem": caminho_imagem,
        "soma_ponderada": float(soma_ponderada),
        "area_por_pixel": float(area_por_pixel),
        "area_normalizada": float(area_normalizada),
        "histograma": histograma
    })
    
def calcular_histograma(imagem_cinza):
    """
    Calcula o histograma das intensidades de pixels de uma imagem em escala de cinza.
    
    :param imagem: A imagem em escala de cinza.
    :return: Frequências das intensidades de 0 a 255.
    """
    histograma, _ = np.histogram(imagem_cinza, bins=np.arange(257))  # Cria histogramas com 256 bins.
    return histograma

def main(imagens, areas_km2):
    """
    Função principal que processa as imagens e calcula a soma ponderada das intensidades.
    
    :param imagens: Lista de caminhos das imagens a serem processadas.
    :param areas_km2: Lista de áreas correspondentes a cada imagem em km².
    :return: Dicionário com resultados de cada imagem.
    """
    if not imagens:
        logging.error("Erro: Nenhuma imagem foi fornecida.")  # Loga erro se nenhuma imagem for fornecida.
        return {}
    
    if len(imagens) != len(areas_km2):
        logging.error("Erro: O número de imagens deve ser igual ao número de áreas.")  # Loga erro se o número de imagens não corresponder.
        return {}

    areas_por_pixel = []  # Lista para armazenar áreas por pixel.
    resultados = []  # Lista para armazenar os resultados.

    # Ler cada imagem e calcular áreas por pixel
    for i, caminho_imagem in enumerate(imagens):
        if areas_km2[i] < 0:
            logging.error(f"Erro: Área negativa fornecida para {caminho_imagem}.")  # Loga erro se a área for negativa.
            continue
        
        imagem = ler_imagem(caminho_imagem)  # Lê a imagem.

        if imagem is None:
            logging.error(f"Erro ao carregar {caminho_imagem}. Verifique se o arquivo é uma imagem válida.")
            continue

        altura, largura, _ = imagem.shape  # Obtém as dimensões da imagem.
        area_por_pixel = calcular_area_por_pixel(areas_km2[i], altura, largura)  # Calcula área por pixel.
        areas_por_pixel.append(area_por_pixel)  # Armazena a área por pixel.

    areas_normalizadas = []  # Lista para áreas normalizadas.
    if not areas_por_pixel:  # Verifica se a lista de áreas por pixel está vazia.
        logging.warning("Nenhuma área válida foi fornecida para normalização.")
    else:
        areas_normalizadas = normalizar_areas(areas_por_pixel)  # Normaliza as áreas.

    # Calcula a soma ponderada das intensidades para cada imagem
    for i, caminho_imagem in enumerate(imagens):
        try:
            imagem = ler_imagem(caminho_imagem)

            if imagem is None:
                registra_processamento(resultados, caminho_imagem, erro_processamento="Erro ao carregar imagem.")
                continue
            
            imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)  # Converte a imagem para escala de cinza.
            soma_ponderada = soma_ponderada_intensidades(imagem_cinza, areas_normalizadas[i])  # Calcula soma ponderada.
            
            histograma = calcular_histograma(imagem_cinza)

            # Armazena os resultados
            registra_processamento(resultados, caminho_imagem, soma_ponderada, areas_por_pixel[i], areas_normalizadas[i], histograma.tolist())
            
            logging.info(f"Soma ponderada para {caminho_imagem}: {soma_ponderada}")  # Loga a soma ponderada.
        except Exception as e:
            message = str(e)  # Captura a mensagem da exceção.
            registra_processamento(resultados, caminho_imagem, erro_processamento=message)  # Registra o erro.
            logging.error(message)  # Loga a mensagem de erro.

    return resultados  # Retorna os resultados.

if __name__ == "__main__":
    configurar_logs()
    
    parser = argparse.ArgumentParser(description="Processar imagens e calcular soma ponderada das intensidades.")
    parser.add_argument('--imagens', nargs='+', help='Caminhos completos das imagens a serem processadas.')
    parser.add_argument('--areas_km', nargs='+', type=float, help='Áreas estimadas em km² para cada imagem.')

    args = parser.parse_args()

    # Verifica se os parâmetros foram passados corretamente
    if args.imagens and args.areas_km and len(args.imagens) == len(args.areas_km):
        resultados = main(args.imagens, args.areas_km)
        if resultados:
            logging.info(f"Resultados: {resultados}")
            print(resultados)
        else:
            print([])
    else:
        logging.error("Erro: O número de imagens deve ser igual ao número de áreas.")
        print([])

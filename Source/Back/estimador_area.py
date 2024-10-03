import cv2
import re
import os

def estimar_area(caminho_imagem, x_m, y_m):
    """
    Estima a área de uma região em uma imagem em km².

    Parâmetros:
    - caminho_imagem: str, caminho da imagem a ser analisada
    - x_m: float, resolução em metros por pixel na direção x
    - y_m: float, resolução em metros por pixel na direção y

    Retorna:
    - float, área em km²
    """
    resultado1 = extrair_area_km2_a_partir_do_nome_imagem(os.path.basename(caminho_imagem))
    return resultado1 if resultado1 else calcular_area(caminho_imagem, x_m, y_m)

def calcular_area(caminho_imagem, resolucao_x, resolucao_y):
    """
    Calcula a área de uma região em uma imagem em km².

    Parâmetros:
    - caminho_imagem: str, caminho da imagem a ser analisada
    - resolucao_x: float, resolução em metros por pixel na direção x
    - resolucao_y: float, resolução em metros por pixel na direção y

    Retorna:
    - float, área em km²
    """
    # 1. Carregar a imagem do mapa
    imagem = cv2.imread(caminho_imagem)

    # 2. Converter para escala de cinza
    imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # 3. Binarizar a imagem (ajuste o limiar conforme necessário)
    _, imagem_binaria = cv2.threshold(imagem_gray, 127, 255, cv2.THRESH_BINARY)

    # 4. Encontrar contornos
    contornos, _ = cv2.findContours(imagem_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 5. Calcular área do contorno
    area_em_pixels = cv2.contourArea(contornos[0])  # Considerando o primeiro contorno

    # 6. Calcular a área em m²
    area_em_m2 = area_em_pixels * (resolucao_x * resolucao_y)  # Área em m²

    # 7. Converter para km²
    area_em_km2 = area_em_m2 / 1_000_000  # 1 km² = 1_000_000 m²

    return area_em_km2

def extrair_area_km2_a_partir_do_nome_imagem(nome_imagem):
    # Expressão regular para encontrar 'area_km2_' seguido de um número (pode ser inteiro ou decimal)
    padrao = r'area_km2_([\d.]+)'
    
    # Realiza a busca no nome da imagem
    resultado = re.search(padrao, nome_imagem)
    
    if resultado:
        # Extrai o valor encontrado e converte para float
        area_km2 = float(resultado.group(1))
        return area_km2
    else:
        # Retorna None se o padrão não for encontrado
        return None
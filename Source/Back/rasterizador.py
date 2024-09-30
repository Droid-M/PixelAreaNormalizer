import os
import argparse
from qgis.core import QgsRasterLayer, QgsProject, QgsApplication, QgsCoordinateTransformContext, QgsRasterBandStats
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
import logging
from datetime import datetime
import warnings

app = QgsApplication([], False)
app.initQgis()

def configurar_logs():
    """
    Configura o sistema de logging para registrar eventos e erros em um arquivo.
    O arquivo de log será chamado 'processamento_imagens.log'.
    """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    logging.basicConfig(
        filename='processamento_imagens.log',  # Nome do arquivo onde os logs serão armazenados.
        level=logging.DEBUG,  # Define o nível de logging; DEBUG para registrar tudo.
        format='%(asctime)s - %(levelname)s - %(message)s'  # Formato das mensagens de log.
    )
    
    # Configurar variáveis de ambiente para suprimir mensagens do GDAL
    os.environ['CPL_DEBUG'] = 'OFF'  # Desativar mensagens de depuração do GDAL
    os.environ['GDAL_SKIP'] = 'gdal'  # Ignorar o driver GDAL que pode causar erros

def calcular_area_pixel(camada, res_x, res_y):
    # Verifica se a camada é válida
    if not camada or not isinstance(camada, QgsRasterLayer):
        logging.error("Camada inválida ou não é uma camada raster.")
        return None
    
    # Verifica se a resolução foi obtida corretamente
    if res_x is None or res_y is None:
        logging.error(f"Não foi possível obter a resolução da camada: {camada.name()}")
        return None
    
    # Calcula a área do pixel em km²
    area_pixel_km2 = (res_x * res_y) / 1_000_000
    
    print(f"Resolução X: {res_x} metros/pixel, Resolução Y: {res_y} metros/pixel")

    
    # Log dos valores de resolução e área por pixel
    logging.info(f"Resolução X: {res_x} metros/pixel, Resolução Y: {res_y} metros/pixel")
    logging.info(f"Área de pixel em km²: {area_pixel_km2:.6f} km²")
    
    return area_pixel_km2

# Configuração do logging
configurar_logs()

# Configuração do argparse para receber múltiplos caminhos de imagem
parser = argparse.ArgumentParser(description='Calcular a área do pixel de imagens raster.')
parser.add_argument('caminhos_imagens', type=str, nargs='+', help='Caminhos para as imagens raster')
args = parser.parse_args()

areas_pixels = []  # Lista para armazenar as áreas
totais_pixels = []  # Lista para armazenar o total de pixels por imagem
caminhos_output = []  # Lista para armazenar os caminhos dos arquivos raster de saída
resultados_processamento = []  # Lista para armazenar os resultados de processamento de cada imagem
maior_area_pixel = 0  # Para determinar a maior área entre as imagens
areas_normalizadas = [] # Para armazenar as areas normalizadas
histogramas = [] # Para armazenar os histogramas

# Processar cada imagem fornecida
for caminho_imagem in args.caminhos_imagens:
    # Criar a camada raster a partir do caminho da imagem
    camada = QgsRasterLayer(caminho_imagem, "Camada Raster")

    # Verificar se a camada foi carregada corretamente
    if not camada.isValid():
        logging.error(f"Não foi possível carregar a camada raster a partir do caminho: {caminho_imagem}")
        continue  # Pula para a próxima imagem

    # Adicionar a camada ao projeto
    QgsProject.instance().addMapLayer(camada)

    # Obtém a resolução X e Y (em metros)
    res_x = camada.rasterUnitsPerPixelX()
    res_y = camada.rasterUnitsPerPixelY()

    # Calcular a área de pixel da camada
    area_pixel = calcular_area_pixel(camada, res_x, res_y)

    if not area_pixel:
        logging.error("Não foi possível calcular a área do pixel para a camada fornecida.")
        continue  # Pula para a próxima imagem

    areas_pixels.append(area_pixel)  # Adiciona à lista
    maior_area_pixel = max(maior_area_pixel, area_pixel)  # Atualiza a maior área

    # Obter dimensões da camada (MxN)
    width = camada.width()
    height = camada.height()
    total_pixels = width * height
    totais_pixels.append(total_pixels)  # Armazena o total de pixels da imagem

    # Log do tamanho da imagem
    logging.info(f"Tamanho da imagem: {width} x {height} pixels (M x N)")
    logging.info(f"Total de pixels: {total_pixels}")

    # Configurar a entrada para a Calculadora Raster
    calc_entry = QgsRasterCalculatorEntry()
    calc_entry.raster = camada
    calc_entry.bandNumber = 1  # Usando a banda 1
    calc_entry.ref = 'layer@1'
    
    # Calcular o histograma da banda 1
    provider = camada.dataProvider()
    histograma = provider.histogram(1)
    
    if histograma:
        # Extrair os dados do histograma
        valores_histograma = list(histograma.histogramVector)  # Retorna um array de valores
        histogramas.append(valores_histograma)  # Adiciona o array de histogramas à lista
        logging.info(f"Histograma calculado para a imagem: {caminho_imagem}")
    else:
        logging.error(f"Erro ao calcular o histograma da imagem: {caminho_imagem}")
        histogramas.append(None) 

    # Normalização da área do pixel
    area_normalizada = area_pixel / maior_area_pixel
    areas_normalizadas.append(area_normalizada)

    # Definir a expressão para multiplicar os valores de cinza pela área normalizada
    expression = f"layer@1 * {area_normalizada}"

    # Log da expressão a ser utilizada
    logging.info(f"Expressão usada na calculadora raster: {expression}")

    # Configurar e rodar a Calculadora Raster
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"./Resultados/Rasters/output_{timestamp}.tif"
    calc = QgsRasterCalculator(
        expression, 
        output_path, 
        "GTiff", 
        camada.extent(),  # Usar a extensão da camada
        width,   # Usar a largura da camada
        height,  # Usar a altura da camada
        [calc_entry],
        QgsCoordinateTransformContext(),
    )

    # Processar o cálculo e salvar a saída
    result = calc.processCalculation()
    resultados_processamento.append(result)  # Adiciona o resultado do processamento

    # Verificar se o cálculo foi bem-sucedido
    if result == 0:  # 0 indica sucesso
        logging.info("Processamento bem-sucedido. Raster salvo em: %s", output_path)
        caminhos_output.append(output_path)  # Adiciona o caminho do arquivo raster de saída
    else:
        logging.error("Erro ao processar a Calculadora Raster.")
        caminhos_output.append(None)  # Adiciona None caso haja erro

# Criar um dicionário com os resultados
print({
    "status": "processamento concluído",
    "maior_area_pixel_km2": maior_area_pixel,
    "areas_pixel_km2": areas_pixels,
    "totais_pixels": totais_pixels,
    "caminhos_output": caminhos_output,
    "resultados_processamento": resultados_processamento,
    "areas_normalizadas": areas_normalizadas,
    "histogramas": histogramas
})

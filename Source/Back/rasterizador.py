import os
import argparse
from qgis.core import QgsRasterLayer, QgsProject, QgsApplication, QgsCoordinateTransformContext
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
    
    # Log dos valores de resolução e área por pixel
    logging.info(f"Resolução X: {res_x} metros/pixel, Resolução Y: {res_y} metros/pixel")
    logging.info(f"Área de pixel em km²: {area_pixel_km2:.6f} km²")
    
    return area_pixel_km2

# Configuração do logging
configurar_logs()

# Configuração do argparse para receber o caminho da imagem
parser = argparse.ArgumentParser(description='Calcular a área do pixel de uma imagem raster.')
parser.add_argument('caminho_imagem', type=str, help='Caminho para a imagem raster')
args = parser.parse_args()

# Caminho da imagem a partir do argumento
caminho_imagem = args.caminho_imagem

# Criar a camada raster a partir do caminho da imagem
camada = QgsRasterLayer(caminho_imagem, "Camada Raster")

# Verificar se a camada foi carregada corretamente
if not camada.isValid():
    logging.error(f"Não foi possível carregar a camada raster a partir do caminho: {caminho_imagem}")
    raise ValueError(f"Não foi possível carregar a camada raster a partir do caminho: {caminho_imagem}")

# Adicionar a camada ao projeto
QgsProject.instance().addMapLayer(camada)

# Obtém a resolução X e Y (em metros)
res_x = camada.rasterUnitsPerPixelX()
res_y = camada.rasterUnitsPerPixelY()

# Calcular a área de pixel da camada
area_pixel = calcular_area_pixel(camada, res_x, res_y)

if not area_pixel:
    logging.error("Não foi possível calcular a área do pixel para a camada fornecida.")
    raise ValueError("Não foi possível calcular a área do pixel para a camada fornecida.")

# Obter dimensões da camada (MxN)
width = camada.width()
height = camada.height()
total_pixels = width * height

# Log do tamanho da imagem
logging.info(f"Tamanho da imagem: {width} x {height} pixels (M x N)")
logging.info(f"Total de pixels: {total_pixels}")

# Configurar a entrada para a Calculadora Raster
calc_entry = QgsRasterCalculatorEntry()
calc_entry.raster = camada
calc_entry.bandNumber = 1  # Usando a banda 1
calc_entry.ref = 'layer@1'

# Definir a expressão para multiplicar os valores de cinza pela área do pixel
expression = f"layer@1 * {area_pixel}"

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

# Verificar se o cálculo foi bem-sucedido
if result == 0:  # 0 indica sucesso
    logging.info("Processamento bem-sucedido. Raster salvo em: %s", output_path)
else:
    logging.error("Erro ao processar a Calculadora Raster.")

# Criar um dicionário com o resultado
print({
    "status": result,
    "erro": None if result == 0 else "Erro ao processar a Calculadora Raster.",
    "output_path": output_path if result == 0 else None,
    "area_pixel_km2": area_pixel,
    "total_pixels": total_pixels,
})
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk  # Necessário para manipulação de imagens
import os
from Back import estimador_area
from tkinter import filedialog, messagebox
from Back.logger import logging

def renderizar_graficos(lista_de_valores, num_barras, caminhos_imagens, titulo_grafico, titulo_metrica, cores = None):
    plt.figure(figsize=(20, 10)) 
    
    # Define os ticks do eixo y
    maior_valor = max(0, max(lista_de_valores))
    ypassos = maior_valor / 20
    plt.yticks(np.arange(0, maior_valor + ypassos, ypassos))
    
    # Gera cores distintas
    if cores is None:
        cores =  plt.cm.viridis(np.linspace(0, 1, num_barras))  # Use uma colormap diferente, como 'viridis'
    
    barras = plt.bar(caminhos_imagens, lista_de_valores, color=cores)
    
    # Adiciona linhas de traçado
    for barra in barras:
        # plt.axhline(y=barra.get_height(), color='red', linestyle='-', alpha=0.2)
        
        # Adiciona o valor dentro da barra
        plt.text(
            barra.get_x() + barra.get_width() / 2,  # Posição X (centro da barra)
            barra.get_height() / 2,                  # Posição Y (metade da altura da barra)
            f'{barra.get_height():.2f}',             # Formata o valor com duas casas decimais
            ha='center',                              # Alinha horizontalmente ao centro
            va='center',                              # Alinha verticalmente ao centro
            color='black'                            # Cor do texto (branco)
        )
        
    plt.title(titulo_grafico)
    plt.ylabel(titulo_metrica)
    plt.xticks(rotation=45, ha='right')  # Rotaciona os rótulos do eixo x
    plt.tight_layout()  # Ajusta o layout
    plt.show()

# Função para criar uma nova janela para o histograma
def mostrar_histogramas(histogramas, caminhos_imagens):
    plt.figure(figsize=(10, 5))
    histogramo_agregado = [0] * 256

    # Soma os histogramas
    for histograma in histogramas:
        histogramo_agregado = [x + y for x, y in zip(histogramo_agregado, histograma)]

    plt.bar(range(256), histogramo_agregado, color='gray', alpha=0.7)
    plt.title('Histograma Agregado de Intensidades')
    plt.xlabel('Intensidade do Pixel')
    plt.ylabel('Frequência Total')
    plt.xlim([0, 255])
    plt.tight_layout()
    plt.show()

# Função para criar uma nova janela para a soma ponderada
def mostrar_soma_ponderada(somas_ponderadas, caminhos_imagens):
    renderizar_graficos(somas_ponderadas, len(somas_ponderadas), caminhos_imagens, 'Somas ponderadas (Consumo de energia)', 'Soma ponderada')

# Função para criar uma nova janela para a área por pixel
def mostrar_areas_por_pixel(areas_por_pixel, caminhos_imagens):
    renderizar_graficos(areas_por_pixel, len(areas_por_pixel), caminhos_imagens, 'Áreas por pixel', 'Área por pixel (km²/pixel)')

# Função para criar uma nova janela para a área normalizada
def mostrar_areas_normalizadas(areas_normalizadas, caminhos_imagens):
    renderizar_graficos(areas_normalizadas, len(areas_normalizadas), caminhos_imagens, 'Áreas normalizadas', 'Área normalizada (km²)')
  
def pedir_dimensao_imagem(caminho):
    """
    Função para criar uma janela de diálogo que pede a dimensão da imagem,
    exibindo a pré-visualização da imagem.

    Args:
        caminho (str): Caminho da imagem.

    Returns:
        float: Dimensão informada pelo usuário em km² ou None se cancelado.
    """
    # Cria uma nova janela
    dialogo = tk.Toplevel()
    dialogo.title("Dimensão da Imagem")
    
    dimensao_resultado = [None] # Para capturar o resultado
    
    # Carrega e exibe a imagem
    img = Image.open(caminho)
    img.thumbnail((300, 300))  # Tamanho máximo da pré-visualização
    img_tk = ImageTk.PhotoImage(img)
    
    label_imagem = tk.Label(dialogo, image=img_tk)
    label_imagem.image = img_tk  # Mantém a referência da imagem
    label_imagem.pack()

    # Campo de entrada para a dimensão
    label_dimensao = tk.Label(dialogo, text="Verifique a dimensão em km² da imagem:")
    label_dimensao.pack(pady=5)
    entry_dimensao = tk.Entry(dialogo)
    entry_dimensao.pack(pady=5)
    
    entry_dimensao.insert(0, estimador_area.estimar_area(caminho, 1, 1))

    # Função para fechar o diálogo e retornar o valor
    def confirmar():
        try:
            dimensao = float(entry_dimensao.get())
            dimensao_resultado[0] = float(entry_dimensao.get())
            dialogo.destroy()  # Fecha a janela
            return dimensao
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido.")
    
    # Botão para confirmar a entrada
    button_confirmar = tk.Button(dialogo, text="Confirmar", command=confirmar)
    button_confirmar.pack(pady=10)

    # Aguarda o fechamento da janela
    dialogo.wait_window(dialogo)
    
    # Retorna a dimensão informada, ou None se a janela foi fechada
    return dimensao_resultado[0]

# Função para selecionar imagens e coletar dimensões
def seletor_de_imagens():
    caminhos_imagens = filedialog.askopenfilenames(
        title="Selecionar Imagens",
        filetypes=[
            ("TIF", "*.tif"),
            ("PNG", "*.png"),
            ("JPEG", "*.jpg"),
            ("JPEG", "*.jpeg"),
            ("BMP", "*.bmp"),
            ("GIF", "*.gif"),
            ("Todas as Imagens", "*.*")
        ]
    )
    if not caminhos_imagens:
        messagebox.showinfo("Informação", "Nenhuma imagem selecionada.")
        return None, None

    dimensoes = []
    for caminho in caminhos_imagens:
        dimensao = pedir_dimensao_imagem(caminho)
        if dimensao is not None:
            dimensoes.append(float(dimensao))
        else:
            messagebox.showwarning("Aviso", "Dimensão não informada. Operação cancelada!")
            return None, None

    logging.debug("Caminhos das Imagens: %s", list(caminhos_imagens))
    logging.debug("Dimensões em km²: %s", dimensoes)
    
    return caminhos_imagens, dimensoes

def mostrar_percentual_consumo_energia(somas_ponderadas, caminhos_imagens):
    """
    Gera um gráfico de pizza exibindo o percentual de consumo de energia
    para cada imagem processada.
    
    Args:
        somas_ponderadas (list): Lista das somas ponderadas de cada imagem.
        caminhos_imagens (list): Lista dos caminhos das imagens correspondentes.
    """

    # Define os rótulos e os valores
    rótulos = [os.path.basename(caminho) for caminho in caminhos_imagens]
    valores = somas_ponderadas

    # Cria o gráfico de pizza
    plt.figure(figsize=(8, 8))
    plt.pie(valores, labels=rótulos, autopct='%1.1f%%', startangle=140)
    plt.title("Percentual de Consumo de Energia por Imagem")
    plt.axis('equal')  # Para garantir que o gráfico seja circular
    plt.show()
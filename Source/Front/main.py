import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import matplotlib.pyplot as plt
import os, sys
import numpy as np

# Adiciona o diretório pai ao caminho
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora faça a importação
from Back.main import main, logging, configurar_logs  # Ajuste a importação para refletir a nova estrutura

# Função para criar uma nova janela para o histograma
def mostrar_histogramas(histogramas, caminhos_imagens):
    plt.figure(figsize=(10, 5))
    for i, histograma in enumerate(histogramas):
        plt.subplot(len(histogramas), 1, i + 1)  # Cria subplots para cada histograma
        plt.bar(range(256), histograma, color='gray', alpha=0.7)
        plt.title(f'Histograma de Intensidades - {caminhos_imagens[i]}')
        plt.xlabel('Intensidade do Pixel')
        plt.ylabel('Frequência')
        plt.xlim([0, 255])
    plt.tight_layout()  # Ajusta o layout
    plt.show()  # Exibe todos os histogramas de uma v

# Função para criar uma nova janela para a soma ponderada
def mostrar_soma_ponderada(somas_ponderadas, caminhos_imagens):
    plt.figure(figsize=(10, 5))  # Tamanho do gráfico
    num_barras = len(somas_ponderadas)
    
    # Gera cores distintas
    cores = plt.cm.viridis(np.linspace(0, 1, num_barras))  # Use a colormap 'viridis'
    
    plt.bar(caminhos_imagens, somas_ponderadas, color=cores)
    plt.title('Soma Ponderada')
    plt.ylabel('Soma Ponderada')
    plt.xticks(rotation=45, ha='right')  # Rotaciona os rótulos do eixo x
    plt.tight_layout()  # Ajusta o layout
    plt.show()

# Função para criar uma nova janela para a área por pixel
def mostrar_areas_por_pixel(areas_por_pixel, caminhos_imagens):
    plt.figure(figsize=(10, 5))  # Tamanho do gráfico
    num_barras = len(areas_por_pixel)
    
    # Gera cores distintas
    cores = plt.cm.plasma(np.linspace(0, 1, num_barras))  # Use uma colormap diferente, como 'plasma'
    
    plt.bar(caminhos_imagens, areas_por_pixel, color=cores)
    plt.title('Área por Pixel')
    plt.ylabel('Área por Pixel (km²/pixel)')
    plt.xticks(rotation=45, ha='right')  # Rotaciona os rótulos do eixo x
    plt.tight_layout()  # Ajusta o layout
    plt.show()

# Função para criar uma nova janela para a área normalizada
def mostrar_areas_normalizadas(area_normalizada, caminhos_imagens):
    plt.figure(figsize=(10, 5))  # Tamanho do gráfico
    num_barras = len(area_normalizada)
    
    # Gera cores distintas
    cores = plt.cm.viridis(np.linspace(0, 1, num_barras))  # Use uma colormap diferente, como 'viridis'
    
    plt.bar(caminhos_imagens, area_normalizada, color=cores)
    plt.title('Área Normalizada')
    plt.ylabel('Área Normalizada')
    plt.xticks(rotation=45, ha='right')  # Rotaciona os rótulos do eixo x
    plt.tight_layout()  # Ajusta o layout
    plt.show()

import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import matplotlib.pyplot as plt
import sys  # Importa o módulo sys

# Funções para criar gráficos (omitidas para brevidade)

# Função principal da interface
def criar_interface(resultados, root):
    somas_ponderadas = []
    caminhos_imagens = []
    areas_por_pixel = []
    areas_normalizadas = []
    histogramas = []
    
    def extrai_resultados(novos_resultados):
        if (novos_resultados):
            somas_ponderadas.clear()
            caminhos_imagens.clear()
            areas_por_pixel.clear()
            areas_normalizadas.clear()
            histogramas.clear()
            for resultado in novos_resultados:
                somas_ponderadas.append(resultado['soma_ponderada'])
                caminhos_imagens.append(resultado['caminho_imagem'])
                areas_por_pixel.append(resultado['area_por_pixel'])
                areas_normalizadas.append(resultado['area_normalizada'])
                histogramas.append(resultado['histograma'])
    
    def selecionar_outras_imagens():
        novos_resultados = selecionar_imagens()
        extrai_resultados(novos_resultados)
            
    def on_soma_ponderada():
        if somas_ponderadas:
            mostrar_soma_ponderada(somas_ponderadas, caminhos_imagens)
    
    
    def on_histograma():
        if histogramas:
            mostrar_histogramas(histogramas, caminhos_imagens)

    def on_area_por_pixel():
        if areas_por_pixel:
            mostrar_areas_por_pixel(areas_por_pixel, caminhos_imagens)

    def on_area_normalizada():
        if areas_normalizadas:
            mostrar_areas_normalizadas(areas_normalizadas, caminhos_imagens)
            
    extrai_resultados(resultados)

    # Remova a criação de uma nova instância de Tk
    root.title("Projeto PixelAreaNormalizer")
    
    # Adiciona botão para carregar imagens
    tk.Button(root, text="Selecionar imagens", command=lambda: selecionar_outras_imagens()).pack(pady=20)
    
    # Adiciona um separador com Canvas
    separator = tk.Canvas(root, height=2, bg="black")  # Define a altura e a cor da linha
    separator.pack(fill=tk.X, padx=5, pady=10)  # Preenche a largura da janela

    # Botões para abrir cada representação
    tk.Button(root, text="Ver histogramas", command=on_histograma).pack(pady=10)
    tk.Button(root, text="Ver soma ponderadas", command=on_soma_ponderada).pack(pady=10)
    tk.Button(root, text="Ver áreas por pixel", command=on_area_por_pixel).pack(pady=10)
    tk.Button(root, text="Ver áreas Normalizadas", command=on_area_normalizada).pack(pady=10)
    
    # Adiciona um separador com Canvas
    separator = tk.Canvas(root, height=2, bg="black")  # Define a altura e a cor da linha
    separator.pack(fill=tk.X, padx=5, pady=10)  # Preenche a largura da janela
    
    # Adiciona botão para sair da aplicação
    tk.Button(root, text="Sair", command=root.destroy).pack(pady=50)

    root.deiconify()  # Mostra a janela principal

    root.mainloop()

# Função para selecionar imagens e coletar dimensões
def selecionar_imagens():
    caminhos_imagens = filedialog.askopenfilenames(
        title="Selecionar Imagens",
        filetypes=[
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
        return

    dimensoes = []
    for caminho in caminhos_imagens:
        dimensao = simpledialog.askfloat("Dimensão da Imagem", f"Informe a dimensão em km² da imagem:\n{caminho}")
        if dimensao is not None:
            dimensoes.append(dimensao)
        else:
            messagebox.showwarning("Aviso", "Dimensão não informada. Operação cancelada!")
            return

    logging.debug("Caminhos das Imagens: %s", list(caminhos_imagens))
    logging.debug("Dimensões em km²: %s", dimensoes)
    
    resultados = main(caminhos_imagens, dimensoes)
    
    logging.info("Resultados: %s", resultados)
    
    print(resultados)
    
    return resultados

# Inicializa a interface gráfica
if __name__ == "__main__":
    configurar_logs()
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    
    root.title("Selecionar Imagens")  # Defina um título para a janela
    root.geometry("800x600")  # Define o tamanho da janela
    root.update_idletasks()  # Atualiza as tarefas pendentes

    # Centraliza a janela
    width = 800  # Largura que definimos
    height = 600  # Altura que definimos
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    try:
        resultados = selecionar_imagens()
        criar_interface(resultados, root)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        try:
            root.destroy()  # Fecha a janela principal após a seleção
        except tk.TclError:
            pass  # Ignora o erro se a janela já estiver destruída
    sys.exit()  # Encerra o programa


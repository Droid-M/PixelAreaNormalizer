import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Necessário para manipulação de imagens
import matplotlib.pyplot as plt
import os, sys
import numpy as np
import subprocess
import json
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

# Funções para criar gráficos (omitidas para brevidade)

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
    label_dimensao = tk.Label(dialogo, text="Informe a dimensão em km² da imagem:")
    label_dimensao.pack(pady=5)
    entry_dimensao = tk.Entry(dialogo)
    entry_dimensao.pack(pady=5)

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

# Função principal da interface
def criar_interface(resultados, root, frame_preview):
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
        novos_resultados = selecionar_outras_imagens_e_prever(frame_preview)
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
    tk.Button(root, text="Ver somas ponderadas", command=on_soma_ponderada).pack(pady=10)
    tk.Button(root, text="Ver áreas por pixel", command=on_area_por_pixel).pack(pady=10)
    tk.Button(root, text="Ver áreas normalizadas", command=on_area_normalizada).pack(pady=10)
    
    # Adiciona um separador com Canvas
    separator = tk.Canvas(root, height=2, bg="black")  # Define a altura e a cor da linha
    separator.pack(fill=tk.X, padx=5, pady=10)  # Preenche a largura da janela
    
    # Adiciona botão para sair da aplicação
    tk.Button(root, text="Sair", command=root.destroy).pack(pady=30)

    root.deiconify()  # Mostra a janela principal

    root.mainloop()
    
def gerar_comando_consulta(caminhos_imagens, dimensoes):
    """
    Esta função gera um comando de consulta com base nos caminhos das imagens e dimensões fornecidos.
    
    Args:
        caminhos_imagens (list): Lista de caminhos das imagens.
        dimensoes (list): Lista de dimensões das áreas em quilômetros.
        
    Returns:
        str: Comando de consulta formatado para ser executado.
    """
    imagens_str = ' '.join(caminhos_imagens)
    dimensoes_str = ' '.join(map(str, dimensoes))
    
    return f"python3 ./Source/Back/main.py --imagens {imagens_str} --areas_km {dimensoes_str}"
    
# Recupera resultados com base em caminhos e dimensões da imagem
def obter_resultados(caminhos_imagens, dimensoes):
    comando = gerar_comando_consulta(caminhos_imagens, dimensoes)
    
    hasError = False
    resultado = []
    
    try:
        # Executa o comando e captura a saída
        saida = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logging.info(f"Saída do comando: {comando}\n{saida.stdout}")
        resultado = saida.stdout
        hasError = saida.stderr or not resultado    
        
        # Substituindo aspas simples por aspas duplas e corrigindo None para null
        resultado = resultado.replace("None", "null").replace("'", '"')
        
        print(json.loads(resultado))
        
        # Converte a representação de string de um dicionário em um dicionário Python usando json.loads
        resultado = json.loads(resultado)
        
        logging.info(f"Resultados obtidos: {resultado}")
    except Exception as e:
        hasError = True
        logging.error(f"Exceção ao executar o comando: {comando}\n{e}")
    
    if hasError:
        logging.error(f"Erro ao executar o comando: {comando}")
        return []
    
    # return main(caminhos_imagens, dimensoes)
    return resultado

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
        dimensao = pedir_dimensao_imagem(caminho)
        if dimensao is not None:
            dimensoes.append(float(dimensao))
        else:
            messagebox.showwarning("Aviso", "Dimensão não informada. Operação cancelada!")
            return

    logging.debug("Caminhos das Imagens: %s", list(caminhos_imagens))
    logging.debug("Dimensões em km²: %s", dimensoes)
    
    resultados = obter_resultados(caminhos_imagens, dimensoes)
    
    logging.info("Resultados: %s", resultados)
    
    # print(resultados)
    
    return resultados

# Função para criar miniaturas
def criar_miniaturas(caminhos_imagens, frame_preview):
    for widget in frame_preview.winfo_children():
        widget.destroy()  # Limpa as pré-visualizações anteriores

    for caminho in caminhos_imagens:
        # Cria um frame para agrupar a miniatura e o nome
        frame_imagem = tk.Frame(frame_preview)

        # Carrega a imagem e cria uma miniatura
        img = Image.open(caminho)
        img.thumbnail((100, 100))  # Define o tamanho da miniatura
        img_tk = ImageTk.PhotoImage(img)

        # Cria um rótulo para a miniatura
        label_imagem = tk.Label(frame_imagem, image=img_tk)
        label_imagem.image = img_tk  # Mantém a referência da imagem
        label_imagem.pack()

        # Cria um rótulo para o caminho ou nome da imagem
        nome_imagem = os.path.basename(caminho)  # Pega apenas o nome do arquivo
        label_nome = tk.Label(frame_imagem, text=nome_imagem, wraplength=100)
        label_nome.pack()

        # Posiciona o frame com a miniatura e o nome
        frame_imagem.pack(side=tk.LEFT, padx=5, pady=5)

# Função para selecionar imagens e exibir miniaturas
def selecionar_outras_imagens_e_prever(frame_preview):
    resultados = selecionar_imagens()
    if resultados:
        criar_miniaturas([r['caminho_imagem'] for r in resultados], frame_preview)
    return resultados

# Inicializa a interface gráfica
if __name__ == "__main__":
    configurar_logs()
    
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    
    root.title("Selecionar Imagens")  # Defina um título para a janela
    root.geometry("800x900")  # Define o tamanho da janela
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
        # Frame para a visualização das miniaturas
        frame_preview = tk.Frame(root)
        frame_preview.pack(pady=10)
        
        resultados = selecionar_outras_imagens_e_prever(frame_preview)
        criar_interface(resultados, root, frame_preview)
    except Exception as e:
        raise e
        print(f"Ocorreu um erro: {e}")
    finally:
        try:
            root.destroy()  # Fecha a janela principal após a seleção
        except tk.TclError:
            pass  # Ignora o erro se a janela já estiver destruída
    sys.exit()  # Encerra o programa


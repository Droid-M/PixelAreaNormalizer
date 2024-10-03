import tkinter as tk
from PIL import Image, ImageTk  # Necessário para manipulação de imagens
import os
import subprocess
import json
from Back.logger import logging
import Front.gerador_elementos as el

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
            el.mostrar_soma_ponderada(somas_ponderadas, caminhos_imagens)
    
    def on_histograma():
        if histogramas:
            el.mostrar_histogramas(histogramas, caminhos_imagens)

    def on_area_por_pixel():
        if areas_por_pixel:
            el.mostrar_areas_por_pixel(areas_por_pixel, caminhos_imagens)

    def on_area_normalizada():
        if areas_normalizadas:
            el.mostrar_areas_normalizadas(areas_normalizadas, caminhos_imagens)
            
    def percentual_consumo_energia():
        if somas_ponderadas:
            el.mostrar_percentual_consumo_energia(somas_ponderadas, caminhos_imagens)
            
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
    tk.Button(root, text="Ver somas ponderadas (Consumo de energia)", command=on_soma_ponderada).pack(pady=10)
    tk.Button(root, text="Ver áreas por pixel", command=on_area_por_pixel).pack(pady=10)
    tk.Button(root, text="Ver áreas normalizadas", command=on_area_normalizada).pack(pady=10)
    tk.Button(root, text="Ver percentual de consumo energético", command=percentual_consumo_energia).pack(pady=10)
    
    # Adiciona um separador com Canvas
    separator = tk.Canvas(root, height=2, bg="black")  # Define a altura e a cor da linha
    separator.pack(fill=tk.X, padx=5, pady=10)  # Preenche a largura da janela
    
    # Adiciona botão para sair da aplicação
    tk.Button(root, text="Sair", command=root.destroy).pack(pady=20)

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
    
    return f"python3 ./Source/Back/pixerizador.py --imagens {imagens_str} --areas_km {dimensoes_str}"
    
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
    caminhos_imagens, dimensoes = el.seletor_de_imagens()
    if caminhos_imagens is not None and dimensoes is not None:
        resultados = obter_resultados(caminhos_imagens, dimensoes)
        logging.info("Resultados: %s", resultados)
        if resultados:
            criar_miniaturas([r['caminho_imagem'] for r in resultados], frame_preview)
        return resultados
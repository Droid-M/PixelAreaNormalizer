import tkinter as tk
import sys
from Back.logger import logging, configurar_logs
from Front import main_frame
from PIL import Image, ImageTk

# Inicializa a interface gráfica
if __name__ == "__main__":
    configurar_logs()
    
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    
    root.title("Selecionar Imagens")  # Defina um título para a janela
    root.geometry("800x900")  # Define o tamanho da janela
    root.update_idletasks()  # Atualiza as tarefas pendentes
    
    image = Image.open('./Assets/ICOs/app.ico')  # Use .png
    photo = ImageTk.PhotoImage(image)

    # Definir o ícone da janela
    root.iconphoto(False, photo)

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
        
        resultados = main_frame.selecionar_outras_imagens_e_prever(frame_preview)
        main_frame.criar_interface(resultados, root, frame_preview)
    except Exception as e:
        raise e
        print(f"Ocorreu um erro: {e}")
    finally:
        try:
            root.destroy()  # Fecha a janela principal após a seleção
        except tk.TclError:
            pass  # Ignora o erro se a janela já estiver destruída
    sys.exit()  # Encerra o programa
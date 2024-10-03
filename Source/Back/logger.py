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
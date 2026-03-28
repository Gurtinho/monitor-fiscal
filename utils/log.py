import logging

# Configuração básica
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        # logging.FileHandler("monitor_fiscal.log"), # Salva num arquivo
        logging.StreamHandler() # Mostra no terminal
    ]
)
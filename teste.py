import os
from dotenv import load_dotenv

# Carrega o arquivo .env que está na mesma pasta
load_dotenv()

# Define a variável buscando do sistema/env
DATABASE_URL = os.getenv("DATABASE_URL")

# Agora o print vai funcionar
print(f"DATABASE_URL carregada: {DATABASE_URL is not None}")
print(f"Valor encontrado: {DATABASE_URL}")
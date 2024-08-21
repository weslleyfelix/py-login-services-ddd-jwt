# config/config.py

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')  # Padrão 'supersecretkey' se a variável não estiver definida

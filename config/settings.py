import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # llama.cpp
    LLAMA_MODEL_PATH = Path(os.getenv('LLAMA_MODEL_PATH')).expanduser()
    LLAMA_CONTEXT_SIZE = int(os.getenv('LLAMA_CONTEXT_SIZE'))
    LLAMA_N_THREADS = int(os.getenv('LLAMA_N_THREADS'))
    
    # System
    BATCH_SIZE = int(os.getenv('BATCH_SIZE'))
    LOG_LEVEL = os.getenv('LOG_LEVEL')
    DATA_DIR = Path(__file__).parent.parent / "data"

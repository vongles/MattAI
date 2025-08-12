from ctypes import *
import numpy as np
from config.settings import Config

class LlamaWrapper:
    def __init__(self):
        self.lib = CDLL('libllama.so')
        self.ctx = None
        self._setup_model()
    
    def _setup_model(self):
        model_path = Config.LLAMA_MODEL_PATH
        self.lib.llama_init.argtypes = [c_char_p, c_int]
        self.lib.llama_init.restype = c_void_p
        self.ctx = self.lib.llama_init(
            model_path.as_posix().encode('utf-8'),
            Config.LLAMA_CONTEXT_SIZE
        )
        
        self.lib.llama_tokenize.argtypes = [
            c_void_p, c_char_p, POINTER(c_int), c_int
        ]
        self.lib.llama_embedding.argtypes = [
            c_void_p, POINTER(c_int), c_int, POINTER(c_float)
        ]
    
    def tokenize(self, text: str) -> list[int]:
        tokens = (c_int * Config.LLAMA_CONTEXT_SIZE)()
        n_tokens = c_int(0)
        
        self.lib.llama_tokenize(
            self.ctx,
            text.encode('utf-8'),
            tokens,
            Config.LLAMA_CONTEXT_SIZE,
            byref(n_tokens)
        )
        
        return list(tokens)[:n_tokens.value]
    
    def get_embedding(self, text: str) -> np.ndarray:
        tokens = self.tokenize(text)
        embedding = (c_float * 384)()
        
        self.lib.llama_embedding(
            self.ctx,
            (c_int * len(tokens))(*tokens),
            len(tokens),
            embedding
        )
        
        return np.array(embedding, dtype=np.float32)
    
    def __del__(self):
        if self.ctx:
            self.lib.llama_free(self.ctx)

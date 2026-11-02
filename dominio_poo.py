from abc import ABC, abstractmethod
from datetime import datetime
from werkzeug.security import check_password_hash

class Entidade(ABC):
    def __init__(self, id: int = None, ativo: bool = True):
        self.__id = id
        self.__ativo = ativo
        self.__criado_em = datetime.now()

    @property
    def id(self): return self.__id
    @property
    def ativo(self): return self.__ativo
    @property
    def criado_em(self): return self.__criado_em

    @abstractmethod
    def to_dict(self) -> dict: pass

class ItemGaleria(Entidade):
    def __init__(self, titulo: str, url_midia: str, categoria_id: int, ano: int, descricao: str = "", visualizacoes: int = 0, id: int = None, ativo: bool = True):
        super().__init__(id=id, ativo=ativo)
        self.__titulo = titulo
        self.__descricao = descricao
        self.__url_midia = url_midia
        self.__categoria_id = categoria_id
        self.__ano = ano
        self.__visualizacoes = visualizacoes

    def to_dict(self) -> dict:
        return {
            "id": self.id, "titulo": self.__titulo, "descricao": self.__descricao,
            "url_midia": self.__url_midia, "categoria_id": self.__categoria_id,
            "ano": self.__ano, "visualizacoes": self.__visualizacoes, "ativo": self.ativo
        }

class Foto(ItemGaleria):
    pass

class Video(ItemGaleria):
    pass

class Administrador(Entidade):
    def __init__(self, usuario: str, senha_hash: str, id: int = 1):
        super().__init__(id=id, ativo=True)
        self.__usuario = usuario
        self.__senha_hash = senha_hash

    def validar_senha(self, senha_digitada: str) -> bool:
        return check_password_hash(self.__senha_hash, senha_digitada)

    def to_dict(self) -> dict:
        return {"id": self.id, "usuario": self.__usuario, "ativo": self.ativo}
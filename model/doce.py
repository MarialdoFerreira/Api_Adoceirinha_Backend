from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base
from model.avaliacao import Avaliacao


class Doce(Base):
    __tablename__ = 'doce'

    id = Column("pk_doce", Integer, primary_key=True)
    descricao = Column(String(140), unique=True)
    genero = Column(String(10))
    imagem = Column(String(120))
    categoria = Column(String(30))
    valor_atual = Column(Float)
    data_cadastro = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o Doce e a avaliação.
    # Essa relação é implicita, não está salva na tabela 'Doce',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    avaliacoes = relationship("Avaliacao")

    def __init__(self, descricao:str, genero:str, imagem:str, categoria:str, valor_atual:float,
                 data_cadastro:Union[DateTime, None] = None):
        """
        Cria um Doce

        Arguments:
            descricao: descrição do Doce.
            genero: Doce se aplica a pessoas do genero Feminino ou Masculino
            imagem: url do arquivo de imagem contido na pasta
            categoria: bolo de Clubes, Datas comemorativas genericas, aniversario, etc
            valor_atual: valor_atual atual para o Doce
            data_cadastro: data de quando o Doce foi castrado à base
        """
        self.descricao = descricao
        self.genero = genero
        self.imagem = imagem
        self.categoria = categoria
        self.valor_atual = valor_atual

        # se não for informada, será o data exata do cadastro no banco
        if data_cadastro:
            self.data_cadastro = data_cadastro

    def adiciona_avaliacao(self, desc_avaliacao:Avaliacao):
        
        """ Adiciona um nova avaliação ao Doce
        """
        self.avaliacoes.append(desc_avaliacao)


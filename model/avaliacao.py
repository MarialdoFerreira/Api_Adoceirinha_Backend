from model import Base


from sqlalchemy import Column, DateTime, ForeignKey, Integer, String


from datetime import datetime
from typing import Union


class Avaliacao(Base):
    __tablename__ = 'avaliacao'

    id = Column(Integer, primary_key=True)
    desc_avaliacao = Column(String(4000))
    data_avaliacao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre a avaliacao e um doce.
    # Aqui está sendo definido a coluna 'doce' que vai guardar
    # a referencia ao doce, a chave estrangeira que relaciona
    # um doce a avaliacao.
    doce = Column(Integer, ForeignKey("doce.pk_doce"), nullable=False)

    def __init__(self, desc_avaliacao:str, data_avaliacao:Union[DateTime, None] = None):
        """
        Cria uma Avaliacao

        Arguments:
            data_avaliacao: avaliacao realizada pela confeitaria.
            data_avaliacao: data da avaliação inicial da confeitaria
        """
        self.desc_avaliacao = desc_avaliacao
        if data_avaliacao:
            self.data_avaliacao = data_avaliacao


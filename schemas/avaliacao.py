from pydantic import BaseModel


class AvaliacaoSchema(BaseModel):
    """ Define como um nova avaliacao a ser inserida deve ser representada
    """
    doce_id: int = 1
    desc_avaliacao: str = "Adoceirinha: doces de qualidade superior!"

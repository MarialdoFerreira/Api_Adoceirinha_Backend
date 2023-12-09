from pydantic import BaseModel
from typing import Optional, List
from model.doce import Doce

from schemas import AvaliacaoSchema


class DoceSchema(BaseModel):
    """ Define como um novo doce a ser inserido deve ser representado
    """
    descricao: str = "Cupcake"
    genero: Optional[str] = "Unisex"
    categoria: str = "Bento Cake"
    valor_atual: float = 45.78
    imagem: Optional[str] = " "


class DoceBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    descricao: str = "Docinho"

class DoceBuscaSchemaId(BaseModel):
    """Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do produto.
    """
    id: str = ''

class ListagemDocesSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    doces:List[DoceSchema]


def apresenta_doces(doces: List[Doce]):
    """ Retorna uma representação do doce seguindo o schema definido em
        DoceViewSchema.
    """
    result = []
    for doce in doces:
        result.append({
            "descricao": doce.descricao,
            "genero": doce.genero,
            "categoria": doce.categoria,
            "valor_atual": doce.valor_atual,
            "imagem": doce.imagem,
            "id": doce.id
        })

    return {"doces": result}


class DoceViewSchema(BaseModel):
    """ Define como um doce será retornado: doce + avaliacoes.
    """
    id: int = 1
    descricao: str = "Happy birthday"
    genero: str = "Unisex"
    categoria: str = "Bento cake"
    valor_atual: float = 55.00
    total_avaliacoes: int = 1
    avaliacoes:List[AvaliacaoSchema]
    imagem: str = []


class DoceDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    descricao: str

def apresenta_doce(doce: Doce):
    """ Retorna uma representação do doce seguindo o schema definido em
        DoceViewSchema.
    """
    return {
        "id": doce.id,
        "descricao": doce.descricao,
        "genero": doce.genero,
        "categoria": doce.categoria,
        "valor_atual": doce.valor_atual,
        "total_avaliacoes": len(doce.avaliacoes),
        "avaliacoes": [{"desc_avaliacao": c.desc_avaliacao} for c in doce.avaliacoes],
        "imagem": doce.imagem
    }

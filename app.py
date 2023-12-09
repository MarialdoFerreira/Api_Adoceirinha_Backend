from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, Flask, request, send_from_directory
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Doce
from logger import logger
from model.avaliacao import Avaliacao
from schemas import *
from flask_cors import CORS
from waitress import serve

from werkzeug.utils import secure_filename
import os


info = Info(title="API Adoceirinha", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
doce_tag = Tag(name="Doces", description="Adição, visualização e remoção de doces à base.")
avaliacao_tag = Tag(name="Avaliacao", description="Adição de uma avaliação da confeitaria ao doce cadastrado")

UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.post('/doce', tags=[doce_tag],
          responses={"200": DoceViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_doce(form: DoceSchema):
    """Adiciona um novo Doce à base de dados

    Retorna uma representação dos doces e avaliações associadas.
    """
    if 'imagem' in request.files:
        imagem = request.files['imagem']        
        if imagem.filename=='':
            error_msg = "Imagem inválida"
            return {"mesage": error_msg}, 409       
        imagem_filename = secure_filename(imagem.filename)
        imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], imagem_filename))     
        imagem_path = os.path.join(app.config['UPLOAD_FOLDER'], imagem_filename)

        doce = Doce(
            descricao=request.form.get('descricao'),
            genero=request.form.get('genero'),
            imagem=imagem_path,
            categoria=request.form.get('categoria'),
            valor_atual=request.form.get('valor_atual'))
    
    else:
        doce = Doce(
        descricao=form.descricao,
        genero=form.genero,
        imagem=form.imagem,
        categoria=form.categoria,
        valor_atual=form.valor_atual)

    try:
        # criando conexão com a base
        session = Session()
        # adicionando doce
        session.add(doce)
        # efetivando o comando de adição do novo item na tabela
        session.commit()
        logger.debug(f"Adicionado doce descrição: '{doce.descricao}'")
        return apresenta_doce(doce), 200

    except IntegrityError as e:
        # como a duplicidade da descricao é a provável razão do IntegrityError
        error_msg = "Doce de mesma descricao já salvo na base :/"
        logger.warning(f"Erro ao adicionar doce '{doce.descricao}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo doce :/"
        logger.warning(f"Erro ao adicionar doce '{doce.descricao}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/doces', tags=[doce_tag],
         responses={"200": ListagemDocesSchema, "404": ErrorSchema})
def get_doces():
    """Faz a busca por todos os Doces cadastrados

    Retorna uma representação da listagem de doces.
    """
    logger.debug(f"Coletando doces ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    doces = session.query(Doce).all()

    if not doces:
        # se não há doces cadastrados
        return {"doces": []}, 200
    else:
        logger.debug(f"%d doces encontrados" % len(doces))
        # retorna a representação de doces
        return apresenta_doces(doces), 200


@app.get('/doce', tags=[doce_tag],
         responses={"200": DoceViewSchema, "404": ErrorSchema})
def get_doce(query: DoceBuscaSchemaId):
    """Faz a busca por um doce a partir do id do doce

    Retorna uma representação dos doces e avaliações associadas.
    """
    doce_id = query.id
    logger.debug(f"Coletando dados sobre doce #{doce_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    doce = session.query(Doce).filter(Doce.id == doce_id).first()

    if not doce:
        # se o doce não foi encontrado
        error_msg = "Doce não encontrado na base :/"
        logger.warning(f"Erro ao buscar doce '{doce_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Doce encontrado: '{doce.descricao}'")
        # retorna a representação de doce
        return apresenta_doce(doce), 200


@app.delete('/doce', tags=[doce_tag],
            responses={"200": DoceDelSchema, "404": ErrorSchema})
def del_doce(query: DoceBuscaSchema):
    """Deleta um Doce a partir da descricao do doce informado

    Retorna uma mensagem de confirmação da remoção.
    """
    doce_descricao = unquote(unquote(query.descricao))
    logger.debug(f"Deletando dados sobre doce #{doce_descricao}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Doce).filter(Doce.descricao == doce_descricao).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado doce #{doce_descricao}")
        return {"mesage": "Doce removido", "id": doce_descricao}
    else:
        # se o doce não foi encontrado
        error_msg = "Doce não encontrado na base :/"
        logger.warning(f"Erro ao deletar doce #'{doce_descricao}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/avaliacao', tags=[avaliacao_tag],
          responses={"200": DoceViewSchema, "404": ErrorSchema})
def add_avaliacao(form: AvaliacaoSchema):
    """Adiciona de uma nova avaliação ao doce cadastrado na base identificado pelo id

    Retorna uma representação dos doces e avaliações associadas.
    """
    doce_id  = form.doce_id

    logger.debug(f"Adicionando avaliações ao doce #{doce_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo doce
    doce = session.query(Doce).filter(Doce.id == doce_id).first()

    if not doce:
        # se doce não encontrado
        error_msg = "Doce não encontrado na base :/"
        logger.warning(f"Erro ao adicionar avaliação ao doce '{doce_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando avaliação
    desc_avaliacao = form.desc_avaliacao
    avaliacao = Avaliacao(desc_avaliacao)

    # adicionando a avaliação ao doce
    doce.adiciona_avaliacao(avaliacao)
    session.commit()

    logger.debug(f"Adicionado avaliação ao doce #{doce_id}")

    # retorna a representação de doce
    return apresenta_doce(doce), 200

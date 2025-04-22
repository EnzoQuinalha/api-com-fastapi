from typing import Union, List
from fastapi import FastAPI, HTTPException, Depends
from model.db
import Database

app = FastAPI()

# Instância do banco de dados
db = Database()

@app.on_event("startup")
def startup_event():
    db.conectar()

@app.on_event("shutdown")
def shutdown_event():
    db.desconectar()

@app.get("/")
def read_hello():
    return {"Hello": "World"}

@app.get('/items/{item_id}/{query}')
def read_item(item_id: int, query: Union[str, None] = None):
    return {'item_id': item_id, 'query': query}

# Endpoints para séries
@app.post("/series/")
def create_serie(titulo: str, descricao: str, ano_lancamento: int, id_categoria: int):
    """
    Endpoint para cadastrar uma nova série.
    """
    query = """
    INSERT INTO serie (titulo, descricao, ano_lancamento, id_categoria)
    VALUES (%s, %s, %s, %s)
    """
    params = (titulo, descricao, ano_lancamento, id_categoria)
    result = db.executar(query, params)
    if result:
        return {"message": "Série cadastrada com sucesso!"}
    raise HTTPException(status_code=500, detail="Erro ao cadastrar série.")

@app.get("/series/", response_model=List[dict])
def list_series():
    """
    Endpoint para listar todas as séries.
    """
    query = """
    SELECT s.id, s.titulo, s.descricao, s.ano_lancamento, c.nome AS categoria
    FROM serie s
    JOIN categoria c ON s.id_categoria = c.id
    """
    result = db.executar(query)
    if result:
        return result.fetchall()
    raise HTTPException(status_code=500, detail="Erro ao listar séries.")

# Endpoints para categorias
@app.post("/categorias/")
def create_categoria(nome: str):
    """
    Endpoint para cadastrar uma nova categoria.
    """
    query = "INSERT INTO categoria (nome) VALUES (%s)"
    params = (nome,)
    result = db.executar(query, params)
    if result:
        return {"message": "Categoria cadastrada com sucesso!"}
    raise HTTPException(status_code=500, detail="Erro ao cadastrar categoria.")

@app.get("/categorias/", response_model=List[dict])
def list_categorias():
    """
    Endpoint para listar todas as categorias.
    """
    query = "SELECT * FROM categoria"
    result = db.executar(query)
    if result:
        return result.fetchall()
    raise HTTPException(status_code=500, detail="Erro ao listar categorias.")

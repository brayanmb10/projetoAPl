from fastapi import APIRouter      # organiza rotas em grupos
from pydantic import BaseModel     # valida os dados que chegam na API
from typing import Optional        # permite campos opcionais
from database import conectar      # nossa função de conexão

router = APIRouter()  

@router.get("/clientes")
def listar_clientes():
    conn = conectar()                        # abre conexão
    cursor = conn.cursor(dictionary=True)    # retorna dicionários em vez de tuplas
    cursor.execute("SELECT * FROM cliente")  # executa o SELECT
    clientes = cursor.fetchall()             # pega todos os resultados
    conn.close()                             # fecha a conexão
    return clientes   

@router.get("/clientes/{id}")
def buscar_cliente(id: int):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cliente WHERE idcliente = %s", (id,))  # %s evita SQL injection
    cliente = cursor.fetchone()   # pega só um resultado
    conn.close()
    if not cliente:               # se não encontrou, avisa
        return {"erro": "Cliente não encontrado"}
    return cliente    

# Modelo de dados — define os campos que o cliente deve ter
class Cliente(BaseModel):
    nome: str                           # obrigatório
    cpf: str                            # obrigatório
    telefone: Optional[str] = None      # opcional
    datacadastro: Optional[str] = None  # opcional
    cidade: Optional[str] = None        # opcional
    uf: Optional[str] = None            # opcional  

    @router.post("/clientes")
def criar_cliente(cliente: Cliente):   # recebe os dados no corpo da requisição
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO cliente (nome, cpf, telefone, datacadastro, cidade, uf)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (cliente.nome, cliente.cpf, cliente.telefone,
         cliente.datacadastro, cliente.cidade, cliente.uf)
    )
    conn.commit()   # confirma a gravação no banco
    conn.close()
    return {"mensagem": "Cliente cadastrado com sucesso"}                 # retorna a lista em JSON             # cria o grupo de rotas
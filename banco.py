import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


# ---------- CONEXÃO E FUNÇÕES BÁSICAS ----------

def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


def consultar(sql, parametros=()):
    conexao = conectar()
    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(sql, parametros)
        linhas = cursor.fetchall()
        cursor.close()
    finally:
        conexao.close()
    return converter(linhas)


def executar(sql, parametros=()):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute(sql, parametros)
        conexao.commit()
        novo_id = cursor.lastrowid
        cursor.close()
    finally:
        conexao.close()
    return novo_id


def converter(linhas):
    # O banco devolve valores em Decimal e datas em date.
    # Aqui viram float e texto "AAAA-MM-DD", que é o formato usado no programa.
    for linha in linhas:
        if "valor" in linha:
            linha["valor"] = float(linha["valor"])
        if "valor_alvo" in linha:
            linha["valor_alvo"] = float(linha["valor_alvo"])
        if "data" in linha:
            linha["data"] = str(linha["data"])
    return linhas


# ---------- RECEITAS ----------

def listar_receitas():
    return consultar("SELECT id, descricao, valor, data FROM receitas ORDER BY data, id")


def inserir_receita(descricao, valor, data):
    return executar(
        "INSERT INTO receitas (descricao, valor, data) VALUES (%s, %s, %s)",
        (descricao, valor, data),
    )


def atualizar_receita(id_receita, descricao, valor):
    executar(
        "UPDATE receitas SET descricao = %s, valor = %s WHERE id = %s",
        (descricao, valor, id_receita),
    )


def remover_receita(id_receita):
    executar("DELETE FROM receitas WHERE id = %s", (id_receita,))


# ---------- DESPESAS ----------

def listar_despesas():
    return consultar("SELECT id, descricao, valor, categoria, data FROM despesas ORDER BY data, id")


def inserir_despesa(descricao, valor, categoria, data):
    return executar(
        "INSERT INTO despesas (descricao, valor, categoria, data) VALUES (%s, %s, %s, %s)",
        (descricao, valor, categoria, data),
    )


def atualizar_despesa(id_despesa, descricao, valor, categoria):
    executar(
        "UPDATE despesas SET descricao = %s, valor = %s, categoria = %s WHERE id = %s",
        (descricao, valor, categoria, id_despesa),
    )


def remover_despesa(id_despesa):
    executar("DELETE FROM despesas WHERE id = %s", (id_despesa,))


def categorias_usadas():
    linhas = consultar("SELECT DISTINCT categoria FROM despesas ORDER BY categoria")
    nomes = []
    for linha in linhas:
        nomes.append(linha["categoria"])
    return nomes


# ---------- METAS DE ECONOMIA ----------

def listar_metas():
    return consultar("SELECT id, nome, valor_alvo FROM metas ORDER BY id")


def inserir_meta(nome, valor_alvo):
    return executar(
        "INSERT INTO metas (nome, valor_alvo) VALUES (%s, %s)",
        (nome, valor_alvo),
    )


def excluir_meta(id_meta):
    executar("DELETE FROM aportes WHERE meta_id = %s", (id_meta,))
    executar("DELETE FROM metas WHERE id = %s", (id_meta,))


def listar_aportes():
    # "descricao" recebe o nome da meta, para o programa tratar aportes como os outros lançamentos
    return consultar(
        "SELECT a.id, m.nome AS descricao, a.valor, a.data "
        "FROM aportes a JOIN metas m ON m.id = a.meta_id "
        "ORDER BY a.data, a.id"
    )


def inserir_aporte(id_meta, valor, data):
    return executar(
        "INSERT INTO aportes (meta_id, valor, data) VALUES (%s, %s, %s)",
        (id_meta, valor, data),
    )


# ---------- CONFIGURAÇÕES ----------

def obter_limite():
    linhas = consultar("SELECT valor FROM configuracoes WHERE chave = %s", ("limite_gastos",))
    if len(linhas) == 0:
        return 0
    return linhas[0]["valor"]


def salvar_limite(valor):
    executar(
        "INSERT INTO configuracoes (chave, valor) VALUES (%s, %s) "
        "ON DUPLICATE KEY UPDATE valor = %s",
        ("limite_gastos", valor, valor),
    )

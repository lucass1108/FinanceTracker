import os
from datetime import date, datetime

from flask import Flask, flash, redirect, render_template, request, url_for

import banco
from main import (
    calcular_guardado_na_meta,
    calcular_saldo,
    calcular_total,
    filtrar_mes,
    formatar_data,
    formatar_mes,
    listar_categorias,
    total_por_categoria,
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave-local-de-desenvolvimento")


# ---------- FILTROS DO TEMPLATE ----------

@app.template_filter("moeda")
def moeda(valor):
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto


@app.template_filter("data_br")
def data_br(data):
    return formatar_data(data)


# ---------- FUNÇÕES AUXILIARES ----------

def hoje():
    return date.today().strftime("%Y-%m-%d")


def ler_valor(texto):
    texto = texto.strip()
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    try:
        valor = float(texto)
    except ValueError:
        return None
    if valor <= 0 or valor > 99999999:
        return None
    return round(valor, 2)


def ler_data(texto):
    try:
        return datetime.strptime(texto, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        return None


def mes_valido(texto):
    if texto is None:
        return False
    try:
        datetime.strptime(texto, "%Y-%m")
        return True
    except ValueError:
        return False


def deslocar_mes(mes, quantidade):
    ano = int(mes[:4])
    numero = int(mes[5:7])
    total = ano * 12 + (numero - 1) + quantidade
    return f"{total // 12:04d}-{total % 12 + 1:02d}"


def voltar():
    mes = request.form.get("mes", "")
    if mes_valido(mes):
        return redirect(url_for("inicio", mes=mes))
    return redirect(url_for("inicio"))


def achar_meta(id_meta):
    for meta in banco.listar_metas():
        if meta["id"] == id_meta:
            return meta
    return None


def mensagem_limite(mes):
    limite = banco.obter_limite()
    if limite <= 0:
        return None
    gasto = calcular_total(filtrar_mes(banco.listar_despesas(), mes))
    if gasto > limite:
        return "ALERTA: você passou do limite de gastos de " + formatar_mes(mes) + ". Gasto: " + moeda(gasto) + " | Limite: " + moeda(limite)
    if gasto >= limite * 0.8:
        percentual = round(gasto / limite * 100, 1)
        return "Atenção: você já usou " + str(percentual) + "% do limite de gastos de " + formatar_mes(mes) + "."
    return None


# ---------- PÁGINA INICIAL ----------

@app.route("/")
def inicio():
    mes = request.args.get("mes")
    if not mes_valido(mes):
        mes = hoje()[:7]

    receitas = banco.listar_receitas()
    despesas = banco.listar_despesas()
    aportes = banco.listar_aportes()

    receitas_mes = filtrar_mes(receitas, mes)
    despesas_mes = filtrar_mes(despesas, mes)
    aportes_mes = filtrar_mes(aportes, mes)

    total_receitas = calcular_total(receitas_mes)
    total_despesas = calcular_total(despesas_mes)
    total_guardado = calcular_total(aportes_mes)

    resumo = {
        "receitas": total_receitas,
        "despesas": total_despesas,
        "guardado": total_guardado,
        "saldo_mes": round(total_receitas - total_despesas - total_guardado, 2),
        "saldo_total": calcular_saldo(receitas, despesas, aportes),
    }

    categorias = []
    totais = total_por_categoria(despesas_mes)
    for nome in totais:
        percentual = 0
        if total_despesas > 0:
            percentual = round(totais[nome] / total_despesas * 100, 1)
        categorias.append({"nome": nome, "total": round(totais[nome], 2), "percentual": percentual})
    categorias.sort(key=lambda item: item["total"], reverse=True)

    metas = []
    for meta in banco.listar_metas():
        guardado = calcular_guardado_na_meta(aportes, meta["nome"])
        percentual = round(guardado / meta["valor_alvo"] * 100, 1)
        metas.append({
            "id": meta["id"],
            "nome": meta["nome"],
            "alvo": meta["valor_alvo"],
            "guardado": guardado,
            "percentual": percentual,
            "largura": max(0, min(100, percentual)),
            "falta": round(max(0, meta["valor_alvo"] - guardado), 2),
        })

    limite = banco.obter_limite()
    limite_info = None
    if limite > 0:
        percentual = round(total_despesas / limite * 100, 1)
        limite_info = {
            "valor": limite,
            "percentual": percentual,
            "largura": min(100, percentual),
            "restante": round(limite - total_despesas, 2),
            "estourou": total_despesas > limite,
        }

    return render_template(
        "index.html",
        mes=mes,
        mes_br=formatar_mes(mes),
        mes_anterior=deslocar_mes(mes, -1),
        mes_proximo=deslocar_mes(mes, 1),
        hoje=hoje(),
        resumo=resumo,
        receitas=list(reversed(receitas_mes)),
        despesas=list(reversed(despesas_mes)),
        aportes=list(reversed(aportes_mes)),
        categorias=categorias,
        categorias_opcoes=listar_categorias(),
        metas=metas,
        limite_info=limite_info,
    )


# ---------- RECEITAS ----------

@app.route("/receitas", methods=["POST"])
def adicionar_receita():
    descricao = request.form.get("descricao", "").strip()
    valor = ler_valor(request.form.get("valor", ""))
    data = ler_data(request.form.get("data", ""))
    if descricao == "" or len(descricao) > 100:
        flash("Informe uma descrição de até 100 caracteres.", "erro")
    elif valor is None:
        flash("Informe um valor maior que zero.", "erro")
    elif data is None:
        flash("Data inválida.", "erro")
    else:
        banco.inserir_receita(descricao, valor, data)
        flash("Receita adicionada!", "ok")
    return voltar()


@app.route("/receitas/<int:id_receita>/remover", methods=["POST"])
def remover_receita(id_receita):
    banco.remover_receita(id_receita)
    flash("Receita removida.", "ok")
    return voltar()


# ---------- DESPESAS ----------

@app.route("/despesas", methods=["POST"])
def adicionar_despesa():
    descricao = request.form.get("descricao", "").strip()
    valor = ler_valor(request.form.get("valor", ""))
    data = ler_data(request.form.get("data", ""))
    categoria = request.form.get("categoria", "")
    if categoria == "__nova__":
        categoria = request.form.get("nova_categoria", "").strip().capitalize()

    if descricao == "" or len(descricao) > 100:
        flash("Informe uma descrição de até 100 caracteres.", "erro")
    elif valor is None:
        flash("Informe um valor maior que zero.", "erro")
    elif data is None:
        flash("Data inválida.", "erro")
    elif categoria == "" or len(categoria) > 50:
        flash("Escolha uma categoria (ou digite o nome da nova).", "erro")
    else:
        banco.inserir_despesa(descricao, valor, categoria, data)
        flash("Despesa adicionada!", "ok")
        aviso = mensagem_limite(data[:7])
        if aviso:
            flash(aviso, "aviso")
    return voltar()


@app.route("/despesas/<int:id_despesa>/remover", methods=["POST"])
def remover_despesa(id_despesa):
    banco.remover_despesa(id_despesa)
    flash("Despesa removida.", "ok")
    return voltar()


# ---------- LIMITE DE GASTOS ----------

@app.route("/limite", methods=["POST"])
def definir_limite():
    valor = ler_valor(request.form.get("valor", ""))
    if valor is None:
        flash("Informe um limite maior que zero.", "erro")
    else:
        banco.salvar_limite(valor)
        flash("Limite de gastos definido!", "ok")
    return voltar()


@app.route("/limite/remover", methods=["POST"])
def remover_limite():
    banco.salvar_limite(0)
    flash("Limite de gastos removido.", "ok")
    return voltar()


# ---------- METAS DE ECONOMIA ----------

@app.route("/metas", methods=["POST"])
def criar_meta():
    nome = request.form.get("nome", "").strip().capitalize()
    valor_alvo = ler_valor(request.form.get("valor_alvo", ""))
    if nome == "" or len(nome) > 100:
        flash("Informe o nome da meta (até 100 caracteres).", "erro")
        return voltar()
    if valor_alvo is None:
        flash("Informe um valor alvo maior que zero.", "erro")
        return voltar()
    for meta in banco.listar_metas():
        if meta["nome"].lower() == nome.lower():
            flash("Já existe uma meta com esse nome.", "erro")
            return voltar()
    banco.inserir_meta(nome, valor_alvo)
    flash("Meta criada: " + nome, "ok")
    return voltar()


@app.route("/metas/<int:id_meta>/guardar", methods=["POST"])
def guardar_na_meta(id_meta):
    meta = achar_meta(id_meta)
    valor = ler_valor(request.form.get("valor", ""))
    if meta is None:
        flash("Meta não encontrada.", "erro")
    elif valor is None:
        flash("Informe um valor maior que zero.", "erro")
    else:
        disponivel = calcular_saldo(banco.listar_receitas(), banco.listar_despesas(), banco.listar_aportes())
        banco.inserir_aporte(id_meta, valor, hoje())
        flash("Guardado em " + meta["nome"] + ": " + moeda(valor), "ok")
        if valor > disponivel:
            flash("Atenção: esse valor é maior que o seu saldo disponível antes de guardar (" + moeda(disponivel) + ").", "aviso")
    return voltar()


@app.route("/metas/<int:id_meta>/retirar", methods=["POST"])
def retirar_da_meta(id_meta):
    meta = achar_meta(id_meta)
    valor = ler_valor(request.form.get("valor", ""))
    if meta is None:
        flash("Meta não encontrada.", "erro")
    elif valor is None:
        flash("Informe um valor maior que zero.", "erro")
    else:
        guardado = calcular_guardado_na_meta(banco.listar_aportes(), meta["nome"])
        if valor > guardado:
            flash("Você só tem " + moeda(guardado) + " guardado em " + meta["nome"] + ".", "erro")
        else:
            banco.inserir_aporte(id_meta, -valor, hoje())
            flash("Retirado de " + meta["nome"] + ": " + moeda(valor), "ok")
    return voltar()


@app.route("/metas/<int:id_meta>/excluir", methods=["POST"])
def excluir_meta(id_meta):
    meta = achar_meta(id_meta)
    if meta is None:
        flash("Meta não encontrada.", "erro")
    elif calcular_guardado_na_meta(banco.listar_aportes(), meta["nome"]) != 0:
        flash("Retire o dinheiro guardado antes de excluir a meta.", "erro")
    else:
        banco.excluir_meta(id_meta)
        flash("Meta excluída.", "ok")
    return voltar()


if __name__ == "__main__":
    app.run(debug=True)

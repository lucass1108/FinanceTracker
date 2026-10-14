from datetime import date, datetime

import mysql.connector

import banco

CATEGORIAS_PADRAO = ["Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Outros"]


# ---------- FUNÇÕES DE ENTRADA ----------

def pedir_valor(pergunta):
    while True:
        try:
            valor = float(input(pergunta))
            if valor <= 0:
                print("O valor precisa ser maior que zero.")
            else:
                return valor
        except ValueError:
            print("Isso não é um número! Tente de novo.")


def pedir_descricao(pergunta):
    while True:
        texto = input(pergunta).strip()
        if texto != "":
            return texto
        print("O texto não pode ficar vazio.")


def pedir_data():
    while True:
        texto = input("Data (DD/MM/AAAA, Enter para hoje): ").strip()
        if texto == "":
            return date.today().strftime("%Y-%m-%d")
        try:
            data = datetime.strptime(texto, "%d/%m/%Y")
            return data.strftime("%Y-%m-%d")
        except ValueError:
            print("Data inválida. Use o formato DD/MM/AAAA.")


def pedir_mes():
    while True:
        texto = input("Mês (MM/AAAA, Enter para o mês atual): ").strip()
        if texto == "":
            return date.today().strftime("%Y-%m")
        try:
            mes = datetime.strptime(texto, "%m/%Y")
            return mes.strftime("%Y-%m")
        except ValueError:
            print("Mês inválido. Use o formato MM/AAAA.")


def listar_categorias():
    # Categorias padrão + as que você criou em despesas anteriores (ficam salvas no banco)
    categorias = list(CATEGORIAS_PADRAO)
    for nome in banco.categorias_usadas():
        existe = False
        for categoria in categorias:
            if categoria.lower() == nome.lower():
                existe = True
        if not existe:
            categorias.insert(len(categorias) - 1, nome)
    return categorias


def pedir_categoria():
    categorias = listar_categorias()
    print("Categorias:")
    numero = 1
    for categoria in categorias:
        print(" ", numero, "-", categoria)
        numero += 1
    while True:
        try:
            escolha = int(input("Escolha a categoria: "))
            if 1 <= escolha <= len(categorias):
                categoria = categorias[escolha - 1]
                if categoria == "Outros":
                    return criar_categoria(categorias)
                return categoria
            print("Esse número não está na lista.")
        except ValueError:
            print("Digite um número inteiro.")


def criar_categoria(categorias):
    nome = input("Nome da nova categoria (Enter para usar 'Outros'): ").strip().capitalize()
    if nome == "":
        return "Outros"
    for categoria in categorias:
        if categoria.lower() == nome.lower():
            return categoria
    return nome


def escolher_tipo():
    while True:
        tipo = input("Digite 1 para Receita ou 2 para Despesa: ")
        if tipo == "1":
            return "receita"
        elif tipo == "2":
            return "despesa"
        print("Opção inválida.")


def pedir_posicao(lista):
    while True:
        try:
            numero = int(input("Número: "))
            if 1 <= numero <= len(lista):
                return numero - 1
            print("Esse número não está na lista.")
        except ValueError:
            print("Digite um número inteiro.")


# ---------- FUNÇÕES DE CÁLCULO ----------

def calcular_total(lancamentos):
    total = 0
    for item in lancamentos:
        total += item["valor"]
    return round(total, 2)


def calcular_saldo(receitas, despesas, aportes):
    saldo = calcular_total(receitas) - calcular_total(despesas) - calcular_total(aportes)
    return round(saldo, 2)


def saldo_atual():
    return calcular_saldo(banco.listar_receitas(), banco.listar_despesas(), banco.listar_aportes())


def calcular_guardado_na_meta(aportes, nome):
    total = 0
    for aporte in aportes:
        if aporte["descricao"] == nome:
            total += aporte["valor"]
    return round(total, 2)


def filtrar_mes(lancamentos, mes):
    resultado = []
    for item in lancamentos:
        if item["data"][:7] == mes:
            resultado.append(item)
    return resultado


def total_por_categoria(despesas):
    totais = {}
    for gasto in despesas:
        categoria = gasto["categoria"]
        if categoria in totais:
            totais[categoria] += gasto["valor"]
        else:
            totais[categoria] = gasto["valor"]
    return totais


def verificar_limite(mes):
    limite = banco.obter_limite()
    if limite <= 0:
        return
    gasto_no_mes = calcular_total(filtrar_mes(banco.listar_despesas(), mes))
    if gasto_no_mes > limite:
        print("ALERTA: você passou do limite de gastos do mês! Gasto:", gasto_no_mes, "| Limite:", limite)
    elif gasto_no_mes >= limite * 0.8:
        percentual = gasto_no_mes / limite * 100
        print("Atenção: você já usou", round(percentual, 1), "% do limite de gastos do mês.")


# ---------- FUNÇÕES DE FORMATAÇÃO ----------

def formatar_data(data):
    partes = data.split("-")
    return partes[2] + "/" + partes[1] + "/" + partes[0]


def formatar_mes(mes):
    partes = mes.split("-")
    return partes[1] + "/" + partes[0]


def mostrar_lista(titulo, lancamentos):
    print(titulo)
    if len(lancamentos) == 0:
        print("  (nenhum lançamento)")
    numero = 1
    for item in lancamentos:
        texto = formatar_data(item["data"]) + " | " + item["descricao"] + " : " + str(item["valor"])
        if "categoria" in item:
            texto += " (" + item["categoria"] + ")"
        print(" ", numero, "-", texto)
        numero += 1


def barra_progresso(percentual):
    if percentual > 100:
        percentual = 100
    cheios = int(percentual / 10)
    return "[" + "#" * cheios + "-" * (10 - cheios) + "]"


def mostrar_objetivos(objetivos, aportes):
    print("--- Metas de economia ---")
    if len(objetivos) == 0:
        print("  (nenhuma meta criada)")
        return
    numero = 1
    for objetivo in objetivos:
        guardado = calcular_guardado_na_meta(aportes, objetivo["nome"])
        alvo = objetivo["valor_alvo"]
        percentual = guardado / alvo * 100
        print(" ", numero, "-", objetivo["nome"])
        print("     ", barra_progresso(percentual), round(percentual, 1), "%")
        print("      Guardado:", guardado, "de", alvo)
        if guardado >= alvo:
            print("      Meta atingida!")
        else:
            print("      Falta:", round(alvo - guardado, 2))
        numero += 1


# ---------- FUNÇÕES DO MENU ----------

def adicionar_receita():
    descricao = pedir_descricao("De onde veio a receita? ")
    valor = pedir_valor("Qual o valor da receita? ")
    data = pedir_data()
    banco.inserir_receita(descricao, valor, data)
    print("Receita adicionada! Saldo disponível:", saldo_atual())


def adicionar_despesa():
    descricao = pedir_descricao("O que foi gasto? ")
    valor = pedir_valor("Qual o valor da despesa? ")
    categoria = pedir_categoria()
    data = pedir_data()
    banco.inserir_despesa(descricao, valor, categoria, data)
    print("Despesa adicionada! Saldo disponível:", saldo_atual())
    verificar_limite(data[:7])


def mostrar_extrato():
    receitas = banco.listar_receitas()
    despesas = banco.listar_despesas()
    aportes = banco.listar_aportes()
    print("--- Extrato ---")
    mostrar_lista("Receitas:", receitas)
    mostrar_lista("Despesas:", despesas)
    mostrar_lista("Guardado em metas (negativo = retirada):", aportes)
    print("Saldo disponível:", calcular_saldo(receitas, despesas, aportes))


def editar_lancamento():
    tipo = escolher_tipo()
    if tipo == "receita":
        lista = banco.listar_receitas()
    else:
        lista = banco.listar_despesas()
    if len(lista) == 0:
        print("Não há lançamentos nessa lista.")
        return
    mostrar_lista("Lançamentos:", lista)
    item = lista[pedir_posicao(lista)]
    nova_descricao = input("Nova descrição (Enter para manter): ").strip()
    if nova_descricao == "":
        nova_descricao = item["descricao"]
    novo_valor = pedir_valor("Novo valor: ")
    if tipo == "receita":
        banco.atualizar_receita(item["id"], nova_descricao, novo_valor)
    else:
        nova_categoria = pedir_categoria()
        banco.atualizar_despesa(item["id"], nova_descricao, novo_valor, nova_categoria)
    print("Lançamento atualizado!")


def remover_lancamento():
    tipo = escolher_tipo()
    if tipo == "receita":
        lista = banco.listar_receitas()
    else:
        lista = banco.listar_despesas()
    if len(lista) == 0:
        print("Não há lançamentos nessa lista.")
        return
    mostrar_lista("Lançamentos:", lista)
    item = lista[pedir_posicao(lista)]
    confirmar = input("Tem certeza que quer remover? (s/n): ").lower()
    if confirmar == "s":
        if tipo == "receita":
            banco.remover_receita(item["id"])
        else:
            banco.remover_despesa(item["id"])
        print("Removido:", item["descricao"], item["valor"])
    else:
        print("Remoção cancelada.")


def mostrar_resumo():
    mes = pedir_mes()
    receitas_mes = filtrar_mes(banco.listar_receitas(), mes)
    despesas_mes = filtrar_mes(banco.listar_despesas(), mes)
    aportes_mes = filtrar_mes(banco.listar_aportes(), mes)
    if len(receitas_mes) == 0 and len(despesas_mes) == 0 and len(aportes_mes) == 0:
        print("Nenhum lançamento em", formatar_mes(mes))
        return

    total_receitas = calcular_total(receitas_mes)
    total_despesas = calcular_total(despesas_mes)
    total_guardado = calcular_total(aportes_mes)
    saldo = round(total_receitas - total_despesas - total_guardado, 2)

    print("--- Resumo de", formatar_mes(mes), "---")
    print("Total de receitas:", total_receitas)
    print("Total de despesas:", total_despesas)
    if len(aportes_mes) > 0:
        print("Guardado em metas no mês:", total_guardado)
    print("Saldo (o que sobra):", saldo)

    if total_receitas > 0:
        percentual = total_despesas / total_receitas * 100
        print("Você já gastou", round(percentual, 1), "% do que ganhou.")

    if len(despesas_mes) > 0:
        maior = despesas_mes[0]
        for gasto in despesas_mes:
            if gasto["valor"] > maior["valor"]:
                maior = gasto
        print("Maior despesa:", maior["descricao"], maior["valor"])

        print("Gastos por categoria:")
        totais = total_por_categoria(despesas_mes)
        for categoria in totais:
            print(" ", categoria, ":", round(totais[categoria], 2))

    limite = banco.obter_limite()
    if limite > 0:
        print("Limite de gastos:", limite, "| Restante:", round(limite - total_despesas, 2))

    if saldo < 0:
        print("Atenção: você está no negativo!")


def definir_limite():
    limite = pedir_valor("Qual o limite de gastos por mês? ")
    banco.salvar_limite(limite)
    print("Limite definido:", limite)


# ---------- FUNÇÕES DAS METAS DE ECONOMIA ----------

def criar_objetivo():
    nome = pedir_descricao("Nome da meta (ex: Viagem, Investimentos): ").capitalize()
    for objetivo in banco.listar_metas():
        if objetivo["nome"].lower() == nome.lower():
            print("Já existe uma meta com esse nome.")
            return
    valor_alvo = pedir_valor("Quanto você quer juntar? ")
    banco.inserir_meta(nome, valor_alvo)
    print("Meta criada:", nome)


def guardar_dinheiro():
    objetivos = banco.listar_metas()
    if len(objetivos) == 0:
        print("Crie uma meta primeiro.")
        return
    mostrar_objetivos(objetivos, banco.listar_aportes())
    objetivo = objetivos[pedir_posicao(objetivos)]
    disponivel = saldo_atual()
    print("Saldo disponível:", disponivel)
    valor = pedir_valor("Quanto você guardou? ")
    if valor > disponivel:
        print("Isso é mais do que o seu saldo disponível.")
        confirmar = input("Registrar mesmo assim? (s/n): ").lower()
        if confirmar != "s":
            print("Operação cancelada.")
            return
    data = pedir_data()
    banco.inserir_aporte(objetivo["id"], valor, data)
    total = calcular_guardado_na_meta(banco.listar_aportes(), objetivo["nome"])
    print("Guardado! Total em", objetivo["nome"] + ":", total)


def retirar_dinheiro():
    objetivos = banco.listar_metas()
    if len(objetivos) == 0:
        print("Crie uma meta primeiro.")
        return
    mostrar_objetivos(objetivos, banco.listar_aportes())
    objetivo = objetivos[pedir_posicao(objetivos)]
    guardado = calcular_guardado_na_meta(banco.listar_aportes(), objetivo["nome"])
    if guardado <= 0:
        print("Não há nada guardado nessa meta.")
        return
    valor = pedir_valor("Quanto você quer retirar? ")
    if valor > guardado:
        print("Você só tem", guardado, "guardado nessa meta.")
        return
    data = pedir_data()
    banco.inserir_aporte(objetivo["id"], -valor, data)
    total = calcular_guardado_na_meta(banco.listar_aportes(), objetivo["nome"])
    print("Retirado! Total em", objetivo["nome"] + ":", total)


def excluir_objetivo():
    objetivos = banco.listar_metas()
    if len(objetivos) == 0:
        print("Não há metas para excluir.")
        return
    mostrar_objetivos(objetivos, banco.listar_aportes())
    objetivo = objetivos[pedir_posicao(objetivos)]
    if calcular_guardado_na_meta(banco.listar_aportes(), objetivo["nome"]) != 0:
        print("Retire o dinheiro guardado antes de excluir a meta.")
        return
    confirmar = input("Tem certeza que quer excluir '" + objetivo["nome"] + "'? (s/n): ").lower()
    if confirmar == "s":
        banco.excluir_meta(objetivo["id"])
        print("Meta excluída.")
    else:
        print("Exclusão cancelada.")


def menu_metas():
    while True:
        print()
        print("--- Metas de economia ---")
        print("1 - Ver metas")
        print("2 - Criar meta")
        print("3 - Guardar dinheiro numa meta")
        print("4 - Retirar dinheiro de uma meta")
        print("5 - Excluir meta")
        print("6 - Voltar")
        opcao = input("O que você quer fazer? ")

        if opcao == "1":
            mostrar_objetivos(banco.listar_metas(), banco.listar_aportes())
        elif opcao == "2":
            criar_objetivo()
        elif opcao == "3":
            guardar_dinheiro()
        elif opcao == "4":
            retirar_dinheiro()
        elif opcao == "5":
            excluir_objetivo()
        elif opcao == "6":
            break
        else:
            print("Opção inválida.")


# ---------- PROGRAMA PRINCIPAL ----------

def main():
    try:
        banco.conectar().close()
    except mysql.connector.Error as erro:
        print("Não foi possível conectar ao banco de dados.")
        print("Confira se o MySQL está rodando e se o arquivo .env está correto.")
        print("Detalhe do erro:", erro)
        return

    print("Bem-vindo ao FinanceTracker!")
    while True:
        print()
        print("1 - Adicionar receita")
        print("2 - Adicionar despesa")
        print("3 - Ver extrato")
        print("4 - Editar lançamento")
        print("5 - Remover lançamento")
        print("6 - Resumo do mês")
        print("7 - Definir limite de gastos do mês")
        print("8 - Metas de economia")
        print("9 - Sair")
        opcao = input("O que você quer fazer? ")

        if opcao == "1":
            adicionar_receita()
        elif opcao == "2":
            adicionar_despesa()
        elif opcao == "3":
            mostrar_extrato()
        elif opcao == "4":
            editar_lancamento()
        elif opcao == "5":
            remover_lancamento()
        elif opcao == "6":
            mostrar_resumo()
        elif opcao == "7":
            definir_limite()
        elif opcao == "8":
            menu_metas()
        elif opcao == "9":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()

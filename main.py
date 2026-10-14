from datetime import date, datetime
 
CATEGORIAS = ["Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Outros"]
 
 
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
 
 
def pedir_categoria():
    print("Categorias:")
    numero = 1
    for categoria in CATEGORIAS:
        print(" ", numero, "-", categoria)
        numero += 1
    while True:
        try:
            escolha = int(input("Escolha a categoria: "))
            if 1 <= escolha <= len(CATEGORIAS):
                categoria = CATEGORIAS[escolha - 1]
                if categoria == "Outros":
                    return criar_categoria()
                return categoria
            print("Esse número não está na lista.")
        except ValueError:
            print("Digite um número inteiro.")
 
 
def criar_categoria():
    nome = input("Nome da nova categoria (Enter para usar 'Outros'): ").strip().capitalize()
    if nome == "":
        return "Outros"
    for categoria in CATEGORIAS:
        if categoria.lower() == nome.lower():
            return categoria
    CATEGORIAS.insert(len(CATEGORIAS) - 1, nome)
    return nome
 
 
def escolher_lista(receitas, despesas):
    while True:
        tipo = input("Digite 1 para Receita ou 2 para Despesa: ")
        if tipo == "1":
            return receitas
        elif tipo == "2":
            return despesas
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
    return total
 
 
def calcular_saldo(receitas, despesas, aportes):
    return calcular_total(receitas) - calcular_total(despesas) - calcular_total(aportes)
 
 
def calcular_guardado_na_meta(aportes, nome):
    total = 0
    for aporte in aportes:
        if aporte["descricao"] == nome:
            total += aporte["valor"]
    return total
 
 
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
 
 
def verificar_limite(despesas, limite, mes):
    if limite <= 0:
        return
    gasto_no_mes = calcular_total(filtrar_mes(despesas, mes))
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
            print("      Falta:", alvo - guardado)
        numero += 1
 
 
# ---------- FUNÇÕES DO MENU ----------
 
def adicionar_receita(receitas, despesas, aportes):
    descricao = pedir_descricao("De onde veio a receita? ")
    valor = pedir_valor("Qual o valor da receita? ")
    data = pedir_data()
    receitas.append({"descricao": descricao, "valor": valor, "data": data})
    print("Receita adicionada! Saldo disponível:", calcular_saldo(receitas, despesas, aportes))
 
 
def adicionar_despesa(receitas, despesas, aportes, configuracao):
    descricao = pedir_descricao("O que foi gasto? ")
    valor = pedir_valor("Qual o valor da despesa? ")
    categoria = pedir_categoria()
    data = pedir_data()
    despesas.append({"descricao": descricao, "valor": valor, "categoria": categoria, "data": data})
    print("Despesa adicionada! Saldo disponível:", calcular_saldo(receitas, despesas, aportes))
    verificar_limite(despesas, configuracao["limite_gastos"], data[:7])
 
 
def mostrar_extrato(receitas, despesas, aportes):
    print("--- Extrato ---")
    mostrar_lista("Receitas:", receitas)
    mostrar_lista("Despesas:", despesas)
    mostrar_lista("Guardado em metas (negativo = retirada):", aportes)
    print("Saldo disponível:", calcular_saldo(receitas, despesas, aportes))
 
 
def editar_lancamento(receitas, despesas):
    lista = escolher_lista(receitas, despesas)
    if len(lista) == 0:
        print("Não há lançamentos nessa lista.")
        return
    mostrar_lista("Lançamentos:", lista)
    posicao = pedir_posicao(lista)
    nova_descricao = input("Nova descrição (Enter para manter): ").strip()
    if nova_descricao != "":
        lista[posicao]["descricao"] = nova_descricao
    lista[posicao]["valor"] = pedir_valor("Novo valor: ")
    if "categoria" in lista[posicao]:
        lista[posicao]["categoria"] = pedir_categoria()
    print("Lançamento atualizado!")
 
 
def remover_lancamento(receitas, despesas):
    lista = escolher_lista(receitas, despesas)
    if len(lista) == 0:
        print("Não há lançamentos nessa lista.")
        return
    mostrar_lista("Lançamentos:", lista)
    posicao = pedir_posicao(lista)
    confirmar = input("Tem certeza que quer remover? (s/n): ").lower()
    if confirmar == "s":
        removido = lista.pop(posicao)
        print("Removido:", removido["descricao"], removido["valor"])
    else:
        print("Remoção cancelada.")
 
 
def mostrar_resumo(receitas, despesas, aportes, configuracao):
    mes = pedir_mes()
    receitas_mes = filtrar_mes(receitas, mes)
    despesas_mes = filtrar_mes(despesas, mes)
    aportes_mes = filtrar_mes(aportes, mes)
    if len(receitas_mes) == 0 and len(despesas_mes) == 0 and len(aportes_mes) == 0:
        print("Nenhum lançamento em", formatar_mes(mes))
        return
 
    total_receitas = calcular_total(receitas_mes)
    total_despesas = calcular_total(despesas_mes)
    total_guardado = calcular_total(aportes_mes)
    saldo = total_receitas - total_despesas - total_guardado
 
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
            print(" ", categoria, ":", totais[categoria])
 
    limite = configuracao["limite_gastos"]
    if limite > 0:
        print("Limite de gastos:", limite, "| Restante:", limite - total_despesas)
 
    if saldo < 0:
        print("Atenção: você está no negativo!")
 
 
def definir_limite(configuracao):
    configuracao["limite_gastos"] = pedir_valor("Qual o limite de gastos por mês? ")
    print("Limite definido:", configuracao["limite_gastos"])
 
 
# ---------- FUNÇÕES DAS METAS DE ECONOMIA ----------
 
def criar_objetivo(objetivos):
    nome = pedir_descricao("Nome da meta (ex: Viagem, Investimentos): ").capitalize()
    for objetivo in objetivos:
        if objetivo["nome"].lower() == nome.lower():
            print("Já existe uma meta com esse nome.")
            return
    valor_alvo = pedir_valor("Quanto você quer juntar? ")
    objetivos.append({"nome": nome, "valor_alvo": valor_alvo})
    print("Meta criada:", nome)
 
 
def guardar_dinheiro(receitas, despesas, objetivos, aportes):
    if len(objetivos) == 0:
        print("Crie uma meta primeiro.")
        return
    mostrar_objetivos(objetivos, aportes)
    posicao = pedir_posicao(objetivos)
    nome = objetivos[posicao]["nome"]
    disponivel = calcular_saldo(receitas, despesas, aportes)
    print("Saldo disponível:", disponivel)
    valor = pedir_valor("Quanto você guardou? ")
    if valor > disponivel:
        print("Isso é mais do que o seu saldo disponível.")
        confirmar = input("Registrar mesmo assim? (s/n): ").lower()
        if confirmar != "s":
            print("Operação cancelada.")
            return
    data = pedir_data()
    aportes.append({"descricao": nome, "valor": valor, "data": data})
    print("Guardado! Total em", nome + ":", calcular_guardado_na_meta(aportes, nome))
 
 
def retirar_dinheiro(objetivos, aportes):
    if len(objetivos) == 0:
        print("Crie uma meta primeiro.")
        return
    mostrar_objetivos(objetivos, aportes)
    posicao = pedir_posicao(objetivos)
    nome = objetivos[posicao]["nome"]
    guardado = calcular_guardado_na_meta(aportes, nome)
    if guardado <= 0:
        print("Não há nada guardado nessa meta.")
        return
    valor = pedir_valor("Quanto você quer retirar? ")
    if valor > guardado:
        print("Você só tem", guardado, "guardado nessa meta.")
        return
    data = pedir_data()
    aportes.append({"descricao": nome, "valor": -valor, "data": data})
    print("Retirado! Total em", nome + ":", calcular_guardado_na_meta(aportes, nome))
 
 
def excluir_objetivo(objetivos, aportes):
    if len(objetivos) == 0:
        print("Não há metas para excluir.")
        return
    mostrar_objetivos(objetivos, aportes)
    posicao = pedir_posicao(objetivos)
    nome = objetivos[posicao]["nome"]
    if calcular_guardado_na_meta(aportes, nome) != 0:
        print("Retire o dinheiro guardado antes de excluir a meta.")
        return
    confirmar = input("Tem certeza que quer excluir '" + nome + "'? (s/n): ").lower()
    if confirmar == "s":
        objetivos.pop(posicao)
        print("Meta excluída.")
    else:
        print("Exclusão cancelada.")
 
 
def menu_metas(receitas, despesas, objetivos, aportes):
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
            mostrar_objetivos(objetivos, aportes)
        elif opcao == "2":
            criar_objetivo(objetivos)
        elif opcao == "3":
            guardar_dinheiro(receitas, despesas, objetivos, aportes)
        elif opcao == "4":
            retirar_dinheiro(objetivos, aportes)
        elif opcao == "5":
            excluir_objetivo(objetivos, aportes)
        elif opcao == "6":
            break
        else:
            print("Opção inválida.")
 
 
# ---------- PROGRAMA PRINCIPAL ----------
 
def main():
    receitas = []
    despesas = []
    objetivos = []
    aportes = []
    configuracao = {"limite_gastos": 0}
 
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
            adicionar_receita(receitas, despesas, aportes)
        elif opcao == "2":
            adicionar_despesa(receitas, despesas, aportes, configuracao)
        elif opcao == "3":
            mostrar_extrato(receitas, despesas, aportes)
        elif opcao == "4":
            editar_lancamento(receitas, despesas)
        elif opcao == "5":
            remover_lancamento(receitas, despesas)
        elif opcao == "6":
            mostrar_resumo(receitas, despesas, aportes, configuracao)
        elif opcao == "7":
            definir_limite(configuracao)
        elif opcao == "8":
            menu_metas(receitas, despesas, objetivos, aportes)
        elif opcao == "9":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")
 
 
if __name__ == "__main__":
    main()
# FinanceTracker

Aplicação de controle financeiro pessoal feita em Python, para rodar no terminal. A ideia é ter uma visão clara do mês: quanto entrou, quanto saiu, quanto foi guardado e quanto ainda sobra do salário.

Projeto pessoal de estudo, desenvolvido por **Lucas** durante o curso de Análise e Desenvolvimento de Sistemas.

## Funcionalidades

- Cadastro de **receitas** (salário e outras entradas) com descrição, valor e data
- Cadastro de **despesas** com descrição, valor, categoria e data
- **Categorias** prontas (Alimentação, Transporte, Moradia, Lazer, Saúde) e opção de criar novas ao escolher "Outros"
- **Extrato** numerado com todos os lançamentos e o saldo disponível
- **Editar** e **remover** lançamentos (com confirmação antes de apagar)
- **Resumo mensal**: receitas, despesas, valor guardado, saldo, percentual gasto, maior despesa e gastos por categoria
- **Limite de gastos** mensal, com aviso ao atingir 80% e alerta ao ultrapassar
- **Metas de economia** (ex: viagem, investimentos, reserva de emergência):
  - criar metas com um valor alvo
  - registrar quanto foi guardado em cada meta (o valor guardado sai do saldo disponível)
  - retirar dinheiro de uma meta
  - acompanhar o progresso com barra e percentual
- Validação de tudo que o usuário digita (valores, datas, meses e opções do menu)

## Como executar

Requisito: Python 3.8 ou superior (não precisa instalar bibliotecas externas).

```bash
python main.py
```

## Menu

```
1 - Adicionar receita
2 - Adicionar despesa
3 - Ver extrato
4 - Editar lançamento
5 - Remover lançamento
6 - Resumo do mês
7 - Definir limite de gastos do mês
8 - Metas de economia
9 - Sair
```

Dentro de **Metas de economia**:

```
1 - Ver metas
2 - Criar meta
3 - Guardar dinheiro numa meta
4 - Retirar dinheiro de uma meta
5 - Excluir meta
6 - Voltar
```

## Estrutura do código

O código está organizado em blocos, cada função com uma responsabilidade:

| Bloco | Funções |
|-------|---------|
| Entrada de dados | `pedir_valor`, `pedir_descricao`, `pedir_data`, `pedir_mes`, `pedir_categoria`, `criar_categoria`, `escolher_lista`, `pedir_posicao` |
| Cálculos | `calcular_total`, `calcular_saldo`, `calcular_guardado_na_meta`, `filtrar_mes`, `total_por_categoria`, `verificar_limite` |
| Formatação | `formatar_data`, `formatar_mes`, `mostrar_lista`, `barra_progresso`, `mostrar_objetivos` |
| Menu | `adicionar_receita`, `adicionar_despesa`, `mostrar_extrato`, `editar_lancamento`, `remover_lancamento`, `mostrar_resumo`, `definir_limite` |
| Metas de economia | `criar_objetivo`, `guardar_dinheiro`, `retirar_dinheiro`, `excluir_objetivo`, `menu_metas` |
| Programa principal | `main` |

Cada lançamento é guardado como um dicionário:

```python
{"descricao": "Mercado", "valor": 400.0, "categoria": "Alimentação", "data": "2026-10-11"}
```

As metas e os valores guardados também são dicionários:

```python
{"nome": "Viagem", "valor_alvo": 2000.0}
{"descricao": "Viagem", "valor": 500.0, "data": "2026-10-11"}
```

## Conceitos praticados

Variáveis e tipos, entrada e saída, condicionais, laços `while` e `for`, listas, dicionários, funções com parâmetros e retorno, tratamento de erros com `try/except`, manipulação de datas com o módulo `datetime` e organização de código.

## Próximos passos

- [ ] Persistência dos dados em banco de dados MySQL
- [ ] Interface web com Flask, HTML e CSS
- [ ] Testes automatizados
- [ ] Exportação de relatórios

## Observação

Atualmente os dados ficam apenas na memória: ao fechar o programa, os lançamentos e as metas são perdidos. Esse é o principal motivo da etapa de banco de dados.

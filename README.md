# FinanceTracker

Aplicação de controle financeiro pessoal feita em Python, para rodar no terminal, com os dados salvos em banco **MySQL**. A ideia é ter uma visão clara do mês: quanto entrou, quanto saiu, quanto foi guardado e quanto ainda sobra do salário.

Projeto pessoal de estudo, desenvolvido por **Lucas** durante o curso de Análise e Desenvolvimento de Sistemas.

## Funcionalidades

- Cadastro de **receitas** (salário e outras entradas) com descrição, valor e data
- Cadastro de **despesas** com descrição, valor, categoria e data
- **Categorias** prontas (Alimentação, Transporte, Moradia, Lazer, Saúde) e opção de criar novas ao escolher "Outros" (as novas ficam salvas)
- **Extrato** numerado com todos os lançamentos e o saldo disponível
- **Editar** e **remover** lançamentos (com confirmação antes de apagar)
- **Resumo mensal**: receitas, despesas, valor guardado, saldo, percentual gasto, maior despesa e gastos por categoria
- **Limite de gastos** mensal, com aviso ao atingir 80% e alerta ao ultrapassar
- **Metas de economia** (ex: viagem, investimentos, reserva de emergência):
  - criar metas com um valor alvo
  - registrar quanto foi guardado em cada meta (o valor guardado sai do saldo disponível)
  - retirar dinheiro de uma meta
  - acompanhar o progresso com barra e percentual
- **Persistência em MySQL**: os dados continuam salvos ao fechar o programa
- Validação de tudo que o usuário digita (valores, datas, meses e opções do menu)

## Tecnologias

- Python 3
- MySQL
- Bibliotecas: `mysql-connector-python` e `python-dotenv`

## Como executar

**1. Instale as dependências**

```bash
pip install -r requirements.txt
```

**2. Crie o banco de dados**

Com o MySQL instalado e rodando, execute o arquivo `schema.sql` (pelo MySQL Workbench ou pelo terminal):

```bash
mysql -u root -p < schema.sql
```

**3. Configure as credenciais**

Copie o arquivo `.env.example` para `.env` e preencha com os seus dados:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=financetracker
```

O arquivo `.env` guarda a senha e **não vai para o GitHub** (está no `.gitignore`).

**4. Rode o programa**

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

## Estrutura do projeto

| Arquivo | Função |
|---------|--------|
| `main.py` | Interface do terminal: menu, entrada de dados, cálculos e exibição |
| `banco.py` | Acesso ao banco: conexão e todas as consultas SQL |
| `schema.sql` | Criação do banco e das tabelas |
| `requirements.txt` | Dependências do projeto |
| `.env.example` | Modelo do arquivo de configuração |

### Banco de dados

| Tabela | Conteúdo |
|--------|----------|
| `receitas` | Entradas de dinheiro |
| `despesas` | Gastos, com categoria |
| `metas` | Metas de economia e valor alvo |
| `aportes` | Dinheiro guardado (positivo) ou retirado (negativo) de cada meta |
| `configuracoes` | Limite de gastos mensal |

### Organização do `main.py`

| Bloco | Funções |
|-------|---------|
| Entrada de dados | `pedir_valor`, `pedir_descricao`, `pedir_data`, `pedir_mes`, `pedir_categoria`, `criar_categoria`, `listar_categorias`, `escolher_tipo`, `pedir_posicao` |
| Cálculos | `calcular_total`, `calcular_saldo`, `saldo_atual`, `calcular_guardado_na_meta`, `filtrar_mes`, `total_por_categoria`, `verificar_limite` |
| Formatação | `formatar_data`, `formatar_mes`, `mostrar_lista`, `barra_progresso`, `mostrar_objetivos` |
| Menu | `adicionar_receita`, `adicionar_despesa`, `mostrar_extrato`, `editar_lancamento`, `remover_lancamento`, `mostrar_resumo`, `definir_limite` |
| Metas de economia | `criar_objetivo`, `guardar_dinheiro`, `retirar_dinheiro`, `excluir_objetivo`, `menu_metas` |
| Programa principal | `main` |

## Conceitos praticados

Variáveis e tipos, entrada e saída, condicionais, laços `while` e `for`, listas, dicionários, funções com parâmetros e retorno, tratamento de erros com `try/except`, manipulação de datas com `datetime`, organização em módulos, SQL (`CREATE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, `JOIN`), consultas parametrizadas, variáveis de ambiente com `.env` e versionamento com Git.

## Próximos passos

- [ ] Interface web com Flask, HTML e CSS
- [ ] Testes automatizados
- [ ] Exportação de relatórios

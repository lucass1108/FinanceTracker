# FinanceTracker

Aplicação de controle financeiro pessoal feita em Python, com **interface web (Flask)** e dados salvos em **MySQL**. A ideia é ter uma visão clara do mês: quanto entrou, quanto saiu, quanto foi guardado e quanto ainda sobra do salário.

Projeto pessoal de estudo, desenvolvido por **Lucas** durante o curso de Análise e Desenvolvimento de Sistemas.

## Funcionalidades

- Cadastro de **receitas** (salário e outras entradas) com descrição, valor e data
- Cadastro de **despesas** com descrição, valor, categoria e data
- **Categorias** prontas (Alimentação, Transporte, Moradia, Lazer, Saúde) e opção de criar novas (ficam salvas)
- **Visão geral do mês**: receitas, despesas, valor guardado, saldo do mês e saldo disponível total
- **Navegação entre meses** para consultar o histórico
- **Gastos por categoria** com percentual de cada uma
- **Remoção** de lançamentos, com confirmação
- **Limite de gastos** mensal, com barra de progresso e aviso ao chegar perto ou ultrapassar
- **Metas de economia** (ex: viagem, investimentos, reserva de emergência):
  - criar metas com um valor alvo
  - registrar quanto foi guardado em cada meta (o valor guardado sai do saldo disponível)
  - retirar dinheiro de uma meta e acompanhar o progresso
- **Persistência em MySQL**: os dados continuam salvos ao fechar o programa
- Validação de todas as entradas (valores, datas, meses, categorias)
- Versão em **terminal** (`main.py`) com as mesmas funções, além do site
- Layout responsivo, com tema claro e escuro automático

## Tecnologias

- Python 3
- Flask (HTML, CSS e templates Jinja)
- MySQL
- Bibliotecas: `flask`, `mysql-connector-python` e `python-dotenv`

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

**4. Rode a aplicação**

Versão web:

```bash
python app.py
```

Depois abra `http://127.0.0.1:5000` no navegador.

Versão terminal:

```bash
python main.py
```

As duas versões usam o mesmo banco de dados.

## Estrutura do projeto

| Arquivo | Função |
|---------|--------|
| `app.py` | Aplicação web: rotas Flask, validações e dados enviados às páginas |
| `templates/index.html` | Página única do site (HTML com Jinja) |
| `static/style.css` | Estilos do site |
| `banco.py` | Acesso ao banco: conexão e todas as consultas SQL |
| `main.py` | Versão para terminal e funções de cálculo compartilhadas |
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

## Conceitos praticados

Variáveis e tipos, condicionais, laços, listas, dicionários, funções, tratamento de erros com `try/except`, manipulação de datas, organização em módulos, SQL (`CREATE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, `JOIN`), consultas parametrizadas, variáveis de ambiente com `.env`, rotas e templates com Flask, formulários HTML, CSS responsivo e versionamento com Git.

## Próximos passos

- [ ] Testes automatizados
- [ ] Edição de lançamentos pelo site
- [ ] Exportação de relatórios
- [ ] Login de usuários

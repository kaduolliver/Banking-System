# Banking System

Projeto feito para o trabalho AT2 de Laborátorio de Banco de Dados, professor William Roberto Malvezzi.

### **Infinity & Legacy** – Sistema bancário robusto e intuitivo

**I&L** Com uma arquitetura moderna baseada em React.js e Tailwind CSS para o frontend, e Python (Flask) com PostgreSQL para o backend, o Infinity & Legacy foi projetado para oferecer uma experiência bancária completa, segura e eficiente.

Desenvolvedores do projeto:

<pre>- Carlos Eduardo Lima de Oliveira</pre>

## ESTRUTURA DO PROJETO

- Separação em front-end e back-end com persistência
- Organização em:
    - `controllers/`: lógica dos endpoints 
    - `routes/`: definição das rotas da API
    - `services/`: lógica de negócios
    - `models/`: estruturação das tabelas do banco
    - `database/`: conexão com banco
    - `client/`: arquivos .JSX, componentes e requisições .js

- Uso do **Flask** como framework de servidor

---

## BANCO DE DADOS (PostgreSQL)

- Estrutura de tabelas (`usuario`, `funcionario`, `cliente` ...)

- Funções (`fn_criar_conta_apos_aprovacao()`, `fn_atualizar_saldo_conta()` ...)

- Triggers (`tg_atualizar_saldo_conta`, `depositar_emprestimo_trigger` ...)

- Procedures (`processar_emprestimo`, `decidir_emprestimo` ...)

- Views (`vw_emprestimos_ativos`)

- Index (`idx_emprestimo_cliente_data`, `idx_transacao_conta_data` ...)

- Uso de `.env` com variáveis de conexão

---


## AUTENTICAÇÃO E SESSÃO

- Registro com senha criptografada `bcrypt`

- Login com validação e uso de `SessionLocal` de SQLAlchemy 

- Armazenar dados do usuário na sessão via `session`

- Logout (destruir sessão) e registro na tabela `auditoria`

---


## React.js NO FRONT-END

- Manipulação do DOM como `document.getElementById` e `innerHTML`

- Escutar eventos `addEventListener`

- Formatação de campos como **Telefone e CPF**

- `fetch()` para consumir a API (GET, POST, PUT, DELETE)

- Manipulação de JSON e tratamento de erros com `try/catch`

---


## API REST com python

- Verbos HTTP: `GET`, `POST`, `PUT`, `DELETE`

- Estrutura de rotas RESTful como `/api/usuario`, `/api/auth/login`

- Corpo da requisição: `application/json`

- Utilização de `Blueprint`

---


## TailwindCSS

- Uso do **TailwindCSS** para responsividade e design moderno

---

## Lógica de Funcionalidades

- Cadastro de clientes e funcionários com validação

- Login com redirecionamento e restrição de falhas

- Painel do `cliente`/`funcionario` (com funções restringidas de acordo com a hierarquia)

- Hierarquia de funcionários `Estagiário`, `Gerente` e `Admin`

- Detalhes de informações sobre conta e capacidade de editar dados

- Solicitação de abertura de conta bancária `Poupança`, `Corrente` e `Investimento`

- Solicitação de `Empréstimos` (com limite de R$ 100.000,00) baseados no score.

- Ações financeiras como `Saque`, `Depósito` e `Transferência` com restrições e taxas

- Geração de `Extratos` exportáveis (PDF)

- Geração de `Relátórios` para funcionários (com restrição de hierarquia)

- Painel de `ativação/desativação` de funcionários para os cargos de administrador


---


## TUTORIAL DE INSTALAÇÃO DO PROJETO

### Pré-requisitos

É necessário ter os seguintes programas instalados:

- PostgreSQL

- Git (para clonar o repositório) **OBS:** caso queira fazer manualmente, pule o passo 1.

### 1. Clonar o repositório
---
<pre>git clone https://github.com/kaduolliver/Banking-System.git

cd Banking-System

code .
</pre>

### 2. Criar o arquivo `.env` na raiz do projeto
---
Crie um arquivo chamado `.env` na raiz com os seguintes dados (ajuste conforme o seu banco de dados local)

Exemplo:
<pre>.env<pre>DB_USER=postgres (por padrão)
DB_HOST=localhost
DB_NAME=seu_banco
DB_PASSWORD=sua_senha
DB_PORT=5432 (por padrão)
SECRET_KEY=sua_key
</pre></pre>

Para gerar uma key digite no terminal:

<pre>
python

import secrets

print(secrets.token_hex(32)) 
</pre>


### 3. Criar o banco de Dados no PostgreSQL
---
Entre no pgAdmin 4 e crie uma nova Database e o mesmo nome que colocar deve por no DB_NAME do `.env`, selecione a database criada e aperte em Query Tool (Alt+Shift+Q), copie os comandos e execute (F5):

<pre>
O arquivo .sql para criar as tabelas/funções/triggers, etc:

Cod. PostgreSQL [atualizado].sql
</pre>

### 3.1 Adicione a `Agência` e o `Admin`/`Gerente`
---
Considerações importantes:

Depois de criar as tabelas/funções, etc. Execute o comando:

<pre>INSERT INTO agencia (nome, codigo_agencia)
VALUES ('Agencia Central', '001');</pre>

Para criar a agência.

Depois de cadastrar 2 funcionários, deve inserir a hierarquia de 'Admin' e 'Gerente':

<pre>UPDATE funcionario
SET cargo = 'Admin',
    nivel_hierarquico = 3,
	inativo = false,
    id_supervisor = NULL,
	codigo_funcionario = NULL
WHERE id_usuario = 1;</pre>

<pre>UPDATE funcionario
SET cargo = 'Gerente',
    nivel_hierarquico = 2,
	inativo = false,
    id_supervisor = 1, 
	codigo_funcionario = NULL 
WHERE id_usuario = 2; </pre>

### 4. Criar ambiente virtual `venv`
---
No terminal (ou prompt de comando), dentro da pastar /server:

<pre>python -m venv venv</pre>

Depois ative:

<pre>venv\Scripts\activate</pre>

### 5. Instalar dependências do requirements.txt
---
Com o (venv) ativado, execute:

<pre>pip install -r requirements.txt</pre>

### 6. Rodar o servidor
---
**Com depêndencias baixadas e .env configurado, execute no /server:**

<pre>python run.py</pre>

Servidor backend ativado! Agora precisamos ativar o frontend.
Não exclua o prompt que esta rodando o backend, crie outro.

### 7. Acessar o Frontend
---
Com outro prompt execute:

<pre>cd /client
npm install</pre>

Aguarde as dependencias do /node_modules baixarem
Então...

<pre>npm run dev</pre>

Acesse a porta http://localhost:5173/ no seu navegador

**Se quiser testar a funcionalidade do QRCode acesse a porta IP da sua máquina**

Abra o cmd e execute:

<pre>ipconfig</pre>

Acesse o IPv4 no seu navegador com a rota :5163/

**QRCode funciona se seu celular e máquina estiver na mesma rede**

---


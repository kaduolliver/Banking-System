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

- Node.js (versão 16+)

- PostgreSQL

- Git (para clonar o repositório) **OBS:** caso queira fazer manualmente, pule o passo 1.

### 1. Clonar o repositório

<pre>git clone https://github.com/kaduolliver/heartcare.git

cd heartcare

code .
</pre>

### 2. Criar o arquivo `.env` na raiz do projeto

Crie um arquivo chamado `.env` na raiz com os seguintes dados (ajuste conforme o seu banco de dados local)

<pre>.env<pre>DB_USER=postgres
DB_HOST=localhost
DB_NAME=heartcare
DB_PASSWORD=12345678
DB_PORT=5432
</pre></pre>

**OBS:**

- **DB_USER** -> é o usuario do PostgreSQL, vem padrão como `postgres`, mas se foi alterado na instalação, será necessário ajustar de acordo;

- **DB_HOST** -> padrão (localhost);

- **DB_NAME** -> é necessário que seja `heartcare` (nome do banco de dados do programa);

- **DB_PASSWORD** -> vai depender de qual senha você colocou ao instalar o PostgreSQL;

- **DB_PORT** -> padrão (5432).

### 3. Criar o banco de Dados no PostgreSQL

Entre no pgAdmin 4 e crie uma nova Database com o nome "heartcare", selecione a database criada e aperte em Query Tool (Alt+Shift+Q), copie os comandos e execute (F5):

<pre>
-- Tabela de usuários
CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  cpf VARCHAR(11) UNIQUE NOT NULL,
  nascimento DATE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  telefone VARCHAR(15) UNIQUE NOT NULL,
  senha VARCHAR(200) NOT NULL,
  sexo VARCHAR(10),
  tipo_sanguineo VARCHAR(5),
  endereco TEXT
);

-- Tabela de médicos
CREATE TABLE medicos (
  crm VARCHAR(20) PRIMARY KEY,
  nome VARCHAR(100),
  especialidade VARCHAR(100)
);

-- Tabela de consultas
CREATE TABLE consultas (
  id SERIAL PRIMARY KEY,
  cpf_usuario VARCHAR(11) REFERENCES usuarios(cpf) ON DELETE CASCADE,
  crm_medico VARCHAR(20) REFERENCES medicos(crm),
  especialidade VARCHAR(100),
  medico VARCHAR(100),
  data_agendamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  data_consulta TIMESTAMP
);
</pre>

### 3.1 Adicione os médicos a tabela `medicos`

<pre>INSERT INTO medicos (crm, nome, especialidade) VALUES
('BA-789.123', 'Dr. Marcelo Henrique Barbosa', 'Cardiologia Geriátrica'),
('CE-567.890', 'Dr. Diego Nascimento Silva', 'Cardiologia de Emergência'),
('DF-345.678', 'Dra. Camila Ribeiro Dias', 'Cardiologia Preventiva'),
('MG-456.789', 'Dra. Fernanda Oliveira Almeida', 'Arritmologia e Eletrofisiologia'),
('PE-876-543', 'Dr. Lucas Pereira Gomes', 'Imagenologia Cardiovascular'),
('PR-654.321', 'Dra. Juliana Costa Lima', 'Cardiologia do Esporte'),
('RJ-987.654', 'Dr. Carlos Eduardo Rocha', 'Cardiologia Intervencionista'),
('RS-321.987', 'Dr. Rafael Torres Almeida', 'Cardiologia Pediátrica'),
('SC-234.567', 'Dra. Patricia Souza Martins', 'Insuficiência Cardíaca e Transplante'),
('SP-123.456', 'Dra. Ana Lucia Mendes', 'Cardiologia Clínica');
</pre>

### 4. Instalar dependências

Dentro da raiz do projeto, rode:

<pre>npm install
</pre>

**Lembrando:** a raiz do projeto é `/heartcare>`

### 5. Rodar o servidor

<pre>node server/server.js

ou

nodemon server/server.js</pre>

O servidor estará disponível em:

`http://localhost:3000`

### 6. Acessar a aplicação

Abra seu navegador e acesse:

<pre>http://localhost:3000
</pre>

### 7. Teste as funcionalidades

- Cadastro: `/pages/register.html`

- Login: `/pages/login.html`

- Área do usuário: `/pages/user.html`

- Agendar Consulta: pela aba "Marcar Consulta"

- Ver Consultas: "Consultas Agendadas"

- Conferir os dados sendo cadastrados dentro do **Banco de Dados**

### 8. Parar o servidor

Pressione `Ctrl + C` no terminal.

## PARA RODAR OS TESTES ##

Agora que todas as dependências estão instaladas e o ambiente está configurado, pode rodar os testes.

Execute no terminal:
<pre>npm run test</pre>


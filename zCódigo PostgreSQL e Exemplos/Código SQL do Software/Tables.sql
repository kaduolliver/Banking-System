CREATE TABLE usuario (
	id_usuario SERIAL PRIMARY KEY,
	nome VARCHAR(255) NOT NULL,
	cpf VARCHAR(11) UNIQUE NOT NULL,
	data_nascimento DATE NOT NULL,
	telefone VARCHAR(20) NOT NULL,
	tipo_usuario VARCHAR(50) NOT NULL CHECK (tipo_usuario IN ('cliente', 'funcionario')),
	senha_hash VARCHAR(255) NOT NULL,
	otp_ativo BOOLEAN DEFAULT FALSE,
	otp_expiracao TIMESTAMP,
	otp_codigo VARCHAR(10) -- ++
);

-- Tabela agencia (atual)

CREATE TABLE agencia (
    id_agencia SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    codigo_agencia VARCHAR(50) UNIQUE NOT NULL
); -- retirado a FK de endereco

CREATE TABLE funcionario (
	id_funcionario SERIAL PRIMARY KEY,
	id_usuario INT UNIQUE NOT NULL,
	codigo_funcionario VARCHAR(50) UNIQUE NOT NULL,
	cargo VARCHAR(100) NOT NULL,
	id_supervisor INT,
	nivel_hierarquico INT,
	id_agencia INT NOT NULL, -- ++
	inativo BOOLEAN DEFAULT TRUE, -- ++ status do funcionario FALSE = ativo / TRUE = inativo (considerar trigger limite de funcionario depois)
	FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
	FOREIGN KEY (id_supervisor) REFERENCES funcionario(id_funcionario),
	FOREIGN KEY (id_agencia) REFERENCES agencia(id_agencia) -- ++
);

CREATE TABLE cliente (
	id_cliente SERIAL PRIMARY KEY,
	id_usuario INT UNIQUE NOT NULL,
	score_credito INT NOT NULL DEFAULT 50 CHECK (score_credito BETWEEN 0 AND 100),
	FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

-- Tabela endereco (atual)

-- 1. Agencia e Admin inseridos via banco de dados 
-- 2. Admin cadastra um endereco para agencia usando id_agencia. OBS: 
CREATE TABLE endereco (
    id_endereco SERIAL PRIMARY KEY,
    id_usuario INT UNIQUE, -- ++ um endereço para cada usuario
    id_agencia INT UNIQUE, -- ++ um endereco para cada agencia
    cep VARCHAR(10) NOT NULL,
    logradouro VARCHAR(255) NOT NULL,
    numero_casa VARCHAR(255) NOT NULL,
    bairro VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    complemento VARCHAR(255),

    CONSTRAINT fk_endereco_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    CONSTRAINT fk_endereco_agencia FOREIGN KEY (id_agencia) REFERENCES agencia(id_agencia), -- ++
	
	-- constraint para vincular o endereco a uma agencia OU usuario, mas nunca para ambos
    CONSTRAINT endereco_usuario_ou_agencia_ck CHECK (
        (id_usuario IS NOT NULL AND id_agencia IS NULL)
        OR
        (id_usuario IS NULL AND id_agencia IS NOT NULL)
    )
);

CREATE TABLE conta (
	id_conta SERIAL PRIMARY KEY,
	numero_conta VARCHAR(30) UNIQUE NOT NULL,
	id_agencia INT NOT NULL,
	saldo NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
	tipo_conta VARCHAR(50) NOT NULL CHECK (tipo_conta IN ('corrente', 'poupanca', 'investimento')),
	id_cliente INT NOT NULL,
	data_abertura DATE NOT NULL DEFAULT CURRENT_DATE,
	status VARCHAR(20) NOT NULL DEFAULT 'ativa',
	FOREIGN KEY (id_agencia) REFERENCES agencia(id_agencia),
	FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
	CONSTRAINT unique_cliente_tipo_conta UNIQUE (id_cliente, tipo_conta) -- ++ apenas um tipo_conta por id_cliente
);

CREATE TABLE conta_poupanca (
	id_conta_poupanca SERIAL PRIMARY KEY,
	id_conta INT UNIQUE NOT NULL,
	taxa_rendimento NUMERIC(5, 4) NOT NULL,
	ultimo_rendimento NUMERIC(15, 2),
	FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
);

CREATE TABLE conta_corrente (
	id_conta_corrente SERIAL PRIMARY KEY,
	id_conta INT UNIQUE NOT NULL,
	limite NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
	data_vencimento DATE,
	taxa_manutencao NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
	FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
);

CREATE TABLE conta_investimento (
	id_conta_investimento SERIAL PRIMARY KEY,
	id_conta INT UNIQUE NOT NULL,
	perfil_risco VARCHAR(50) NOT NULL CHECK (perfil_risco IN ('conservador', 'moderado', 'arrojado')),
	valor_minimo NUMERIC(15, 2) NOT NULL DEFAULT 0.00,
	taxa_rendimento_base NUMERIC(5, 4) NOT NULL,
	FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
);

CREATE TABLE transacao (
	id_transacao SERIAL PRIMARY KEY,
	id_conta_origem INT NOT NULL,
	id_conta_destino INT,
	tipo_transacao VARCHAR(50) NOT NULL CHECK (tipo_transacao IN ('deposito', 'saque', 'transferencia')),
	valor NUMERIC(15, 2) NOT NULL,
	data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	descricao TEXT,
	FOREIGN KEY (id_conta_origem) REFERENCES conta(id_conta),
	FOREIGN KEY (id_conta_destino) REFERENCES conta(id_conta)
);

CREATE TABLE emprestimo (
	id_emprestimo SERIAL PRIMARY KEY,
	id_cliente INT NOT NULL,
	id_conta INT NOT NULL,
	valor_solicitado NUMERIC(15, 2) NOT NULL,
	taxa_juros_mensal NUMERIC(5, 2) NOT NULL,
    finalidade VARCHAR(100),
	prazo_meses INT NOT NULL CHECK (prazo_meses BETWEEN 6 AND 60),
	valor_total NUMERIC(15, 2) NOT NULL,
	data_solicitacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	data_aprovacao TIMESTAMP,
	status VARCHAR(20) NOT NULL DEFAULT 'PENDENTE' CHECK (status IN ('PENDENTE', 'APROVADO', 'REJEITADO', 'PAGO')),
	score_risco NUMERIC(5, 2),
	FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
	FOREIGN KEY (id_conta) REFERENCES conta(id_conta)
);

CREATE TABLE auditoria (
	id_auditoria SERIAL PRIMARY KEY,
	id_usuario INT,
	acao VARCHAR(100) NOT NULL,
	data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	detalhes TEXT,
	FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE relatorio (
	id_relatorio SERIAL PRIMARY KEY,
	id_funcionario INT NOT NULL,
	tipo_relatorio VARCHAR(100) NOT NULL,
	data_geracao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	conteudo TEXT,
	FOREIGN KEY (id_funcionario) REFERENCES funcionario(id_funcionario)
);

-- ++ solicitacao enviada para o funcionario com cargo de gerente ou superior para aprovar/rejeitar
CREATE TABLE solicitacao_conta (
  id_solicitacao SERIAL PRIMARY KEY,
  id_cliente INT NOT NULL,
  tipo_conta VARCHAR(50) NOT NULL CHECK (tipo_conta IN ('corrente', 'poupanca', 'investimento')),
  data_solicitacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(20) NOT NULL DEFAULT 'PENDENTE' CHECK (status IN ('PENDENTE', 'APROVADO', 'REJEITADO')),
  id_funcionario_aprovador INT,
  data_aprovacao TIMESTAMP,
  observacoes TEXT,
  valor_inicial NUMERIC (15, 2) DEFAULT 0.00,
  
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
  FOREIGN KEY (id_funcionario_aprovador) REFERENCES funcionario(id_funcionario)
);
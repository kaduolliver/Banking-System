-- COMANDOS IMPORTANTES PARA INSERIR NO BANCO DE DADOS DEPOIS DE CRIAR AS TABELAS
-- E ANTES DE PROSSEGUIR PARA A APLICAÇÃO

-- OBS 1: Adicione apenas depois de criar as tabelas.
-- OBS 2: Sem essas etapas não tem como prosseguir com a aplicação.

-- Adicionar Agencia

INSERT INTO agencia (nome, codigo_agencia)
VALUES ('Agencia Central', '001')

-- Adicionar Admin

UPDATE funcionario
SET codigo_funcionario = 'ADM001',
    cargo = 'Admin',
    nivel_hierarquico = 3,
    id_supervisor = NULL -- NULL porque admin não tem supervisor
WHERE id_usuario = 1; -- quem será o admin

-- Adicionar Gerente (Opcional)

UPDATE funcionario
SET codigo_funcionario = 'GER001',
    cargo = 'Gerente',
    nivel_hierarquico = 2,
    id_supervisor = 1 -- id_usuario do supervisor [Admin]
WHERE id_usuario = 2; -- quem será o gerente

--OBS 3: Todo funcionario cadastrado no sistema começa como estagiário.


-------------------------TABELAS E FUNÇÕES-------------------------------------

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

CREATE TABLE funcionario (
	id_funcionario SERIAL PRIMARY KEY,
	id_usuario INT UNIQUE NOT NULL,
	codigo_funcionario VARCHAR(50) UNIQUE NOT NULL,
	cargo VARCHAR(100) NOT NULL,
	id_supervisor INT,
	id_agencia INT NOT NULL, -- ++
	FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
	FOREIGN KEY (id_supervisor) REFERENCES funcionario(id_funcionario),
	FOREIGN KEY (id_agencia) REFERENCES agencia(id_agencia) -- ++
);

CREATE TABLE cliente (
	id_cliente SERIAL PRIMARY KEY,
	id_usuario INT UNIQUE NOT NULL,
	score_credito NUMERIC(5, 2),
	FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

-- Tabela agencia (antiga)

-- CREATE TABLE agencia (
-- 	id_agencia SERIAL PRIMARY KEY,
-- 	nome VARCHAR(255) NOT NULL,
-- 	codigo_agencia VARCHAR(50) UNIQUE NOT NULL,
-- 	endereco_id INT UNIQUE NOT NULL,
-- 	FOREIGN KEY (endereco_id) REFERENCES endereco(id_endereco)
-- );

-- Tabela agencia (atual)

CREATE TABLE agencia (
    id_agencia SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    codigo_agencia VARCHAR(50) UNIQUE NOT NULL
); -- retirado a FK de endereco

-- Tabela endereco (antiga)

-- CREATE TABLE endereco (
-- 	id_endereco SERIAL PRIMARY KEY,
-- 	id_usuario INT NOT NULL,
-- 	cep VARCHAR(10) NOT NULL,
-- 	logradouro VARCHAR(255) NOT NULL,
-- 	numero_casa VARCHAR(255) NOT NULL,
-- 	bairro VARCHAR(100) NOT NULL,
-- 	estado CHAR(2) NOT NULL,
-- 	complemento VARCHAR(255),
-- 	FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
-- );

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
	numero_conta VARCHAR(20) UNIQUE NOT NULL,
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

-- Função auditoria
CREATE OR REPLACE FUNCTION fn_registrar_auditoria(p_id_usuario INT, p_acao VARCHAR, p_detalhes TEXT)
RETURNS VOID AS $$
BEGIN
  INSERT INTO auditoria (id_usuario, acao, detalhes)
  VALUES (p_id_usuario, p_acao, p_detalhes);
END;
$$ LANGUAGE plpgsql;

-- Função empréstimo
CREATE OR REPLACE FUNCTION fn_depositar_emprestimo()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.status = 'APROVADO' AND OLD.status IS DISTINCT FROM 'APROVADO' THEN
    INSERT INTO transacao (
      id_conta_origem, tipo_transacao, valor, data_hora, descricao
    ) VALUES (
      NEW.id_conta, 'deposito', NEW.valor_solicitado, CURRENT_TIMESTAMP,
      CONCAT('Empréstimo ID ', NEW.id_emprestimo)
    );
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Função criar conta após aprovação (antigo)
-- CREATE OR REPLACE FUNCTION fn_criar_conta_apos_aprovacao()
-- RETURNS TRIGGER AS $$
-- DECLARE
--   v_numero_conta VARCHAR(20);
--   v_id_agencia INTEGER;
-- BEGIN
--   IF NEW.status = 'APROVADO' AND (OLD.status IS DISTINCT FROM 'APROVADO') THEN
--     -- Gerar número da conta
--     v_numero_conta := 'AC' || TO_CHAR(NOW(), 'YYYYMMDDHH24MISS') || NEW.id_solicitacao;

--     -- Buscar dinamicamente o ID da agência com código '001'
--     SELECT id_agencia INTO v_id_agencia
--     FROM agencia
--     WHERE codigo = '001'
--     LIMIT 1;

--     -- Verificar se a agência foi encontrada
--     IF v_id_agencia IS NULL THEN
--       RAISE EXCEPTION 'Agência com código 001 não encontrada. Verifique se ela foi cadastrada.';
--     END IF;

--     -- Inserir conta vinculada à agência encontrada
--     INSERT INTO conta (
--       numero_conta, id_agencia, saldo, tipo_conta, id_cliente, data_abertura, status
--     ) VALUES (
--       v_numero_conta, v_id_agencia, 0.00, NEW.tipo_conta, NEW.id_cliente, CURRENT_DATE, 'ativa'
--     );
--   END IF;
--   RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- Função criar conta apos aprovação (novo/atual)
CREATE OR REPLACE FUNCTION fn_criar_conta_apos_aprovacao()
RETURNS TRIGGER AS $$
DECLARE
    v_numero_conta VARCHAR(20);
    v_id_agencia INTEGER;
BEGIN
    IF NEW.status = 'APROVADO' AND (OLD.status IS DISTINCT FROM 'APROVADO') THEN
        -- Gerar número da conta
        v_numero_conta := 'AC' || TO_CHAR(NOW(), 'YYYYMMDDHH24MISS') || NEW.id_solicitacao;

        -- Buscar o ID da agência do funcionário aprovador
        SELECT f.id_agencia INTO v_id_agencia
        FROM funcionario f
        WHERE f.id_funcionario = NEW.id_funcionario_aprovador;

        -- Verificar se a agência foi encontrada
        IF v_id_agencia IS NULL THEN
            RAISE EXCEPTION 'Agência do funcionário aprovador (ID: %) não encontrada.', NEW.id_funcionario_aprovador;
        END IF;

        -- Inserir conta vinculada à agência encontrada
        INSERT INTO conta (
            numero_conta, id_agencia, saldo, tipo_conta, id_cliente, data_abertura, status
        ) VALUES (
            v_numero_conta, v_id_agencia, COALESCE(NEW.valor_inicial, 0.00), NEW.tipo_conta, NEW.id_cliente, CURRENT_DATE, 'ativa'
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- ++ Função de limites de funcionarios por agencia
CREATE OR REPLACE FUNCTION fn_verificar_limite_funcionarios_agencia()
RETURNS TRIGGER AS $$
DECLARE
    total_funcionarios INT;
BEGIN
    
    SELECT COUNT(*) INTO total_funcionarios
    FROM funcionario
    WHERE id_agencia = NEW.id_agencia
      AND (TG_OP = 'INSERT' OR id_funcionario != NEW.id_funcionario);  -- evita contar a si mesmo no UPDATE

    IF total_funcionarios >= 20 THEN
        RAISE EXCEPTION 'Limite máximo de 20 funcionários por agência atingido (agência ID: %)', NEW.id_agencia;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Trigger para empréstimo
CREATE TRIGGER depositar_emprestimo
AFTER UPDATE ON emprestimo
FOR EACH ROW
EXECUTE FUNCTION fn_depositar_emprestimo();

-- Trigger para criar conta
CREATE TRIGGER trg_criar_conta_apos_aprovacao
AFTER UPDATE ON solicitacao_conta
FOR EACH ROW
EXECUTE FUNCTION fn_criar_conta_apos_aprovacao();

-- ++ Trigger para limite de funcionarios
CREATE TRIGGER trg_limite_funcionarios_agencia
BEFORE INSERT OR UPDATE ON funcionario
FOR EACH ROW
EXECUTE FUNCTION fn_verificar_limite_funcionarios_agencia();


-- View empréstimos ativos
CREATE OR REPLACE VIEW vw_emprestimos_ativos AS
SELECT
	e.id_emprestimo,
	u.nome,
	e.valor_solicitado,
	e.taxa_juros_mensal,
	e.prazo_meses,
	e.valor_total
FROM emprestimo e
JOIN cliente c ON e.id_cliente = c.id_cliente
JOIN usuario u ON c.id_usuario = u.id_usuario
WHERE e.status = 'APROVADO';

-- Procedure processar_emprestimo
CREATE OR REPLACE PROCEDURE processar_emprestimo(
	IN p_id_cliente INT,
	IN p_id_conta INT,
	IN p_valor NUMERIC(15, 2),
	IN p_prazo INT,
	IN p_finalidade VARCHAR(50),
	IN p_score_risco NUMERIC(5, 2),
	IN p_aprovado BOOLEAN
)
LANGUAGE plpgsql
AS $$
DECLARE
	v_taxa NUMERIC(5, 2);
	v_valor_total NUMERIC(15, 2);
	v_id_emprestimo INT;
BEGIN
	INSERT INTO emprestimo (
		id_cliente, id_conta, valor_solicitado, prazo_meses, score_risco, status, finalidade
	) VALUES (
		p_id_cliente, p_id_conta, p_valor, p_prazo, p_score_risco, 'PENDENTE', p_finalidade
	)
	RETURNING id_emprestimo INTO v_id_emprestimo;

	IF p_aprovado THEN
		v_taxa := CASE
			WHEN p_score_risco <= 20 THEN 0.5
			WHEN p_score_risco <= 40 THEN 1.0
			WHEN p_score_risco <= 60 THEN 2.0
			WHEN p_score_risco <= 80 THEN 3.5
			ELSE 5.0
		END;
		v_valor_total := p_valor * POWER(1 + v_taxa / 100, p_prazo);
		UPDATE emprestimo
		SET status = 'APROVADO',
			taxa_juros_mensal = v_taxa,
			valor_total = v_valor_total,
			data_aprovacao = CURRENT_TIMESTAMP
		WHERE id_emprestimo = v_id_emprestimo;
	ELSE
		UPDATE emprestimo
		SET status = 'REJEITADO'
		WHERE id_emprestimo = v_id_emprestimo;
	END IF;
END;
$$;

CREATE INDEX idx_emprestimo_cliente_data ON emprestimo (id_cliente, data_solicitacao);
CREATE INDEX idx_transacao_conta_data ON transacao(id_conta_origem, data_hora DESC);
CREATE INDEX idx_emprestimo_aprovado ON emprestimo (id_cliente, data_solicitacao) WHERE status = 'APROVADO';

CREATE UNIQUE INDEX idx_usuario_cpf ON usuario(cpf);
CREATE UNIQUE INDEX idx_conta_numero ON conta(numero_conta);
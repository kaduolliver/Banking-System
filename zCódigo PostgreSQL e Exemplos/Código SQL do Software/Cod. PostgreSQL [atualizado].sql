-- COMANDOS IMPORTANTES PARA INSERIR NO BANCO DE DADOS DEPOIS DE CRIAR AS TABELAS
-- E ANTES DE PROSSEGUIR PARA A APLICAÇÃO

-- OBS 1: Adicione apenas depois de criar as tabelas.
-- OBS 2: Sem essas etapas não tem como prosseguir com a aplicação.

-- Adicionar Agencia

INSERT INTO agencia (nome, codigo_agencia)
VALUES ('Agencia Central', '001');

-- Adicionar Admin

UPDATE funcionario
SET cargo = 'Admin',
    nivel_hierarquico = 3,
	inativo = false, -- o status do admin nunca deve ser true
    id_supervisor = NULL, -- NULL porque admin não tem supervisor
	codigo_funcionario = NULL -- obrigatório para funcionar com a função/trigger de incremento
WHERE id_usuario = 1; -- quem será o admin

-- Adicionar Gerente

UPDATE funcionario
SET cargo = 'Gerente',
    nivel_hierarquico = 2,
	inativo = false, -- false para entrar com funcionario ativo
    id_supervisor = 1, -- id_usuario do supervisor [Admin]
	codigo_funcionario = NULL -- obrigatório para funcionar com a função/trigger de incremento
WHERE id_usuario = 2; -- quem será o gerente

--OBS 3: Todo funcionario cadastrado no sistema começa como estagiário.

-- Mudar score_credito do cliente

UPDATE cliente
SET score_credito = 95 -- Determine o score aqui. Emprestimo -> if score_credito >= 80 else "REJEITADO"
WHERE id_cliente = 1; -- Substitua 1 pelo id_cliente do cliente

-- Mudar limite da conta corrente:

UPDATE conta_corrente
SET limite = 5000.00
WHERE id_conta_corrente = 1;


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
	otp_codigo VARCHAR(10), -- ++
    tentativas_login_falhas INTEGER NOT NULL DEFAULT 0, -- ++
    data_bloqueio TIMESTAMP NULL -- ++
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
    valor_taxa NUMERIC(15, 2) DEFAULT 0.00,
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
    id_funcionario_aprovador INT, -- ++ identificar o funcionario que aprova o emprestimo na auditoria
	FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
	FOREIGN KEY (id_conta) REFERENCES conta(id_conta),
    FOREIGN KEY (id_funcionario_aprovador) REFERENCES funcionario(id_funcionario) -- ++ fk funcionario aprovador
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

-- Função que deposita o valor do empréstimo na conta assim que o status é APROVADO
CREATE OR REPLACE FUNCTION fn_depositar_emprestimo_na_conta()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'APROVADO'
        AND (TG_OP = 'INSERT' OR OLD.status IS DISTINCT FROM 'APROVADO') THEN

        INSERT INTO transacao (
            id_conta_origem,
            id_conta_destino,
            tipo_transacao,
            valor,
            data_hora,
            descricao
        ) VALUES (
            NEW.id_conta,
            NULL,
            'deposito',
            NEW.valor_solicitado,
            CURRENT_TIMESTAMP,
            CONCAT('Depósito de Empréstimo ID ', NEW.id_emprestimo, ' aprovado.')
        );

        PERFORM fn_registrar_auditoria(
            NEW.id_funcionario_aprovador, 
            'EMPRESTIMO_DEPOSITADO',
            CONCAT('Depósito de Empréstimo ID ', NEW.id_emprestimo, ' de R$', NEW.valor_solicitado, ' aprovado e depositado na conta ID ', NEW.id_conta, ' pelo funcionário ID ', NEW.id_funcionario_aprovador)
        );

    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- ++ Função para atualizar o saldo do saque/deposito/emprestimo
CREATE OR REPLACE FUNCTION fn_atualizar_saldo_conta()
RETURNS TRIGGER AS $$
DECLARE
    v_tipo_conta              TEXT;
    v_saldo                   NUMERIC(15,2);
    v_limite                  NUMERIC(15,2) := 0;
    v_total_depositos_hoje    NUMERIC(15,2);
    v_total_saques_hoje       NUMERIC(15,2);
    LIMITE_DEPOSITO_DIARIO_PADRAO NUMERIC(15,2) := 10000.00; -- Limite de R$ 10.000,00 para depósitos normais
    LIMITE_SAQUE_DIARIO       NUMERIC(15,2) := 5000.00; -- NOVO: Limite de R$ 5.000,00 para saques diários
BEGIN

    SELECT c.tipo_conta,
           c.saldo,
           COALESCE(cc.limite, 0)
    INTO   v_tipo_conta,
           v_saldo,
           v_limite
    FROM   conta c
    LEFT JOIN conta_corrente cc USING (id_conta)
    WHERE  c.id_conta = NEW.id_conta_origem;

    IF NEW.tipo_transacao IN ('saque', 'transferencia') THEN
        IF (v_saldo + CASE WHEN v_tipo_conta = 'corrente' THEN v_limite ELSE 0 END) < NEW.valor THEN
            RAISE EXCEPTION 'Saldo (incluindo limite) insuficiente na conta de origem.';
        END IF;
    END IF;

    IF NEW.tipo_transacao = 'deposito' THEN

        IF NEW.descricao LIKE 'Depósito de Empréstimo ID %' THEN
            
            NULL;
        ELSE

            SELECT COALESCE(SUM(valor), 0)
            INTO v_total_depositos_hoje
            FROM transacao
            WHERE id_conta_origem = NEW.id_conta_origem
              AND tipo_transacao = 'deposito'
              AND data_hora::DATE = CURRENT_DATE
              AND descricao NOT LIKE 'Depósito de Empréstimo ID %';

            IF (v_total_depositos_hoje + NEW.valor) > LIMITE_DEPOSITO_DIARIO_PADRAO THEN
                RAISE EXCEPTION 'Limite de depósito diário de R$ % atingido para esta conta. Total depositado hoje: R$ %. Depósito atual: R$ %.',
                                 LIMITE_DEPOSITO_DIARIO_PADRAO, v_total_depositos_hoje, NEW.valor;
            END IF;
        END IF;
    ELSIF NEW.tipo_transacao = 'saque' THEN
        SELECT COALESCE(SUM(valor), 0)
        INTO v_total_saques_hoje
        FROM transacao
        WHERE id_conta_origem = NEW.id_conta_origem
          AND tipo_transacao = 'saque'
          AND data_hora::DATE = CURRENT_DATE;

        IF (v_total_saques_hoje + NEW.valor) > LIMITE_SAQUE_DIARIO THEN
            RAISE EXCEPTION 'Limite de saque diário de R$ % atingido para esta conta. Total sacado hoje: R$ %. Saque atual: R$ %.',
                            LIMITE_SAQUE_DIARIO, v_total_saques_hoje, NEW.valor;
        END IF;
    END IF;

    -- Atualiza o saldo de acordo com o tipo de transação
    IF NEW.tipo_transacao = 'deposito' THEN
        UPDATE conta
        SET saldo = saldo + NEW.valor
        WHERE id_conta = NEW.id_conta_origem;

    ELSIF NEW.tipo_transacao = 'saque' THEN
        UPDATE conta
        SET saldo = saldo - NEW.valor
        WHERE id_conta = NEW.id_conta_origem;

    ELSIF NEW.tipo_transacao = 'transferencia' THEN
        UPDATE conta
        SET saldo = saldo - NEW.valor
        WHERE id_conta = NEW.id_conta_origem;

        UPDATE conta
        SET saldo = saldo + NEW.valor
        WHERE id_conta = NEW.id_conta_destino;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Função criar conta apos aprovação (novo/atual)
CREATE OR REPLACE FUNCTION fn_criar_conta_apos_aprovacao()
RETURNS TRIGGER AS $$
DECLARE
    v_numero_base TEXT;
    v_numero_conta VARCHAR(30);
    v_id_agencia INTEGER;
    v_id_nova_conta INT;
    v_dv INT;
    v_soma INT := 0;
    v_char CHAR;
    v_digit INT;
    v_nome_cliente VARCHAR(255); 
BEGIN
    IF NEW.status = 'APROVADO' AND (OLD.status IS DISTINCT FROM 'APROVADO') THEN

        v_numero_base := TO_CHAR(NOW(), 'YYYYMMDDHH24MISS') || NEW.id_solicitacao;

        FOR i IN 1..LENGTH(v_numero_base) LOOP
            v_char := SUBSTRING(v_numero_base FROM i FOR 1);
            IF v_char ~ '[0-9]' THEN
                v_digit := CAST(v_char AS INT);
                v_soma := v_soma + v_digit;
            END IF;
        END LOOP;

        v_dv := v_soma % 10;

        v_numero_conta := 'BR' || v_numero_base || v_dv;

        SELECT f.id_agencia INTO v_id_agencia
        FROM funcionario f
        WHERE f.id_funcionario = NEW.id_funcionario_aprovador;

        IF v_id_agencia IS NULL THEN
            RAISE EXCEPTION 'Agência do funcionário aprovador (ID: %) não encontrada.', NEW.id_funcionario_aprovador;
        END IF;

        SELECT u.nome INTO v_nome_cliente
        FROM cliente c
        JOIN usuario u ON c.id_usuario = u.id_usuario
        WHERE c.id_cliente = NEW.id_cliente;

        INSERT INTO conta (
            numero_conta, id_agencia, saldo, tipo_conta, id_cliente, data_abertura, status
        ) VALUES (
            v_numero_conta, v_id_agencia, COALESCE(NEW.valor_inicial, 0.00),
            NEW.tipo_conta, NEW.id_cliente, CURRENT_DATE, 'ativa'
        )
        RETURNING id_conta INTO v_id_nova_conta;

        IF NEW.tipo_conta = 'poupanca' THEN
            INSERT INTO conta_poupanca (id_conta, taxa_rendimento, ultimo_rendimento)
            VALUES (v_id_nova_conta, 0.005, 0.00);
        ELSIF NEW.tipo_conta = 'corrente' THEN
            INSERT INTO conta_corrente (id_conta, limite, data_vencimento, taxa_manutencao)
            VALUES (v_id_nova_conta, 0.00, CURRENT_DATE + INTERVAL '1 year', 0.00);
        ELSIF NEW.tipo_conta = 'investimento' THEN
            INSERT INTO conta_investimento (id_conta, perfil_risco, valor_minimo, taxa_rendimento_base)
            VALUES (v_id_nova_conta, 'conservador', 0.00, 0.009);
        END IF;
       
        PERFORM fn_registrar_auditoria(
            NEW.id_funcionario_aprovador, 
            'ABERTURA_CONTA_APROVADA',
            CONCAT('Nova conta ', NEW.tipo_conta, ' (Nº ', v_numero_conta, ') aberta para o cliente ', v_nome_cliente, ' (ID: ', NEW.id_cliente, ').')
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


-- Função de incremento no código do Gerente e Admin
CREATE OR REPLACE FUNCTION gerar_codigo_funcionario()
RETURNS TRIGGER AS $$
DECLARE
    prefixo TEXT;
    ultimo_codigo TEXT;
    numero_inteiro INTEGER;
BEGIN
    IF (TG_OP = 'INSERT' AND NEW.codigo_funcionario IS NULL)
       OR (TG_OP = 'UPDATE' AND NEW.codigo_funcionario IS DISTINCT FROM OLD.codigo_funcionario AND NEW.cargo <> OLD.cargo) THEN

        IF NEW.cargo = 'Admin' THEN
            prefixo := 'ADM';
        ELSIF NEW.cargo = 'Gerente' THEN
            prefixo := 'GER';
        ELSE
            prefixo := 'EST';
        END IF;

        SELECT MAX(codigo_funcionario)
        INTO ultimo_codigo
        FROM funcionario
        WHERE codigo_funcionario LIKE prefixo || '%';

        IF ultimo_codigo IS NOT NULL THEN
            numero_inteiro := CAST(SUBSTRING(ultimo_codigo FROM '[0-9]+$') AS INTEGER) + 1;
        ELSE
            numero_inteiro := 1;
        END IF;

        NEW.codigo_funcionario := prefixo || LPAD(numero_inteiro::TEXT, 3, '0');
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Função para registrar o login de um usuário (funcionário ou cliente)
CREATE OR REPLACE FUNCTION fn_registrar_login(p_id_usuario INT)
RETURNS VOID AS $$
DECLARE
    v_tipo_usuario VARCHAR(50);
    v_nome_usuario VARCHAR(255);
BEGIN
    SELECT tipo_usuario, nome INTO v_tipo_usuario, v_nome_usuario
    FROM usuario
    WHERE id_usuario = p_id_usuario;

    IF v_tipo_usuario IS NOT NULL THEN
        PERFORM fn_registrar_auditoria(
            p_id_usuario,
            'LOGIN',
            CONCAT('Usuário ', v_nome_usuario, ' (', v_tipo_usuario, ') realizou login.')
        );
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Função para registrar o logout de um usuário (funcionário ou cliente)
CREATE OR REPLACE FUNCTION fn_registrar_logout(p_id_usuario INT)
RETURNS VOID AS $$
DECLARE
    v_tipo_usuario VARCHAR(50);
    v_nome_usuario VARCHAR(255);
BEGIN
    SELECT tipo_usuario, nome INTO v_tipo_usuario, v_nome_usuario
    FROM usuario
    WHERE id_usuario = p_id_usuario;

    IF v_tipo_usuario IS NOT NULL THEN
        PERFORM fn_registrar_auditoria(
            p_id_usuario,
            'LOGOUT',
            CONCAT('Usuário ', v_nome_usuario, ' (', v_tipo_usuario, ') realizou logout.')
        );
    END IF;
END;
$$ LANGUAGE plpgsql;


-- Trigger para atualizar saldo
CREATE TRIGGER tg_atualizar_saldo_conta
BEFORE INSERT ON transacao
FOR EACH ROW
EXECUTE FUNCTION fn_atualizar_saldo_conta();

-- Trigger para empréstimo
CREATE OR REPLACE TRIGGER depositar_emprestimo_trigger
AFTER INSERT OR UPDATE ON emprestimo
FOR EACH ROW
EXECUTE FUNCTION fn_depositar_emprestimo_na_conta();

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

-- ++ Trigger de incremento codigo admin/gerente
CREATE TRIGGER trigger_gerar_codigo_funcionario_insert
BEFORE INSERT ON funcionario
FOR EACH ROW
WHEN (NEW.codigo_funcionario IS NULL)
EXECUTE FUNCTION gerar_codigo_funcionario();

-- ++ Trigger para gerar o código do funcionario (de acordo com o cargo)
CREATE TRIGGER trigger_gerar_codigo_funcionario_update
BEFORE UPDATE ON funcionario
FOR EACH ROW
WHEN (
    NEW.codigo_funcionario IS DISTINCT FROM OLD.codigo_funcionario AND
    NEW.cargo <> OLD.cargo
)
EXECUTE FUNCTION gerar_codigo_funcionario();

-- View empréstimos ativos para gerar relatório
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

-- Procedure para processar os emprestimos e setar limite
CREATE OR REPLACE PROCEDURE processar_emprestimo(
    IN p_id_cliente      INT,
    IN p_id_conta        INT,
    IN p_valor           NUMERIC(15,2),
    IN p_prazo           INT,
    IN p_finalidade      VARCHAR(100),
    IN p_score_risco     NUMERIC(5,2)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_status            VARCHAR(20) := 'PENDENTE';
    v_taxa              NUMERIC(5,2) := 0;
    v_valor_total       NUMERIC(15,2) := p_valor;
    LIMITE_VALOR_EMPRESTIMO NUMERIC(15,2) := 100000.00; -- Limite de R$ 100.000,00 para cada empréstimo
BEGIN

    IF p_valor > LIMITE_VALOR_EMPRESTIMO THEN
        RAISE EXCEPTION 'O valor solicitado para o empréstimo (R$ %) excede o limite máximo de R$ %.', p_valor, LIMITE_VALOR_EMPRESTIMO;
    END IF;

    -- Aprovação automática dependendo do score
    IF p_score_risco >= 80 THEN
        v_status := 'APROVADO';
        v_taxa   := 0.5;
        v_valor_total := p_valor * POWER(1 + v_taxa/100, p_prazo);

    -- Rejeição automática dependendo do score
    ELSIF p_score_risco < 40 THEN
        v_status := 'REJEITADO';
    END IF;

    INSERT INTO emprestimo (
        id_cliente, id_conta, valor_solicitado, prazo_meses, score_risco,
        status, finalidade, taxa_juros_mensal, valor_total, data_aprovacao
    ) VALUES (
        p_id_cliente, p_id_conta, p_valor, p_prazo, p_score_risco,
        v_status, p_finalidade, v_taxa, v_valor_total,
        CASE WHEN v_status IN ('APROVADO', 'REJEITADO') THEN CURRENT_TIMESTAMP ELSE NULL END
    );
END;
$$;

-- Procedure para aprovar emprestimo
CREATE OR REPLACE PROCEDURE decidir_emprestimo(
    IN p_id_emprestimo INT,
    IN p_aprovado BOOLEAN,
    IN p_id_funcionario INT 
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_score NUMERIC(5,2);
    v_taxa NUMERIC(5,2) := 0;
    v_valor NUMERIC(15,2);
    v_valor_total NUMERIC(15,2);
    v_prazo INT;
BEGIN
    IF p_aprovado THEN
        -- Busca dados do empréstimo
        SELECT score_risco, valor_solicitado, prazo_meses
        INTO v_score, v_valor, v_prazo
        FROM emprestimo
        WHERE id_emprestimo = p_id_emprestimo;

        -- Define taxa baseada no score
        v_taxa := CASE
                      WHEN v_score >= 80 THEN 0.5
                      WHEN v_score >= 60 THEN 1.0
                      WHEN v_score >= 40 THEN 2.0
                      ELSE 3.0
                  END;

        -- Calcula valor total com juros compostos mensais
        v_valor_total := v_valor * POWER(1 + v_taxa / 100, v_prazo);

        -- Atualiza empréstimo
        UPDATE emprestimo
        SET status = 'APROVADO',
            data_aprovacao = CURRENT_TIMESTAMP,
            taxa_juros_mensal = v_taxa,
            valor_total = v_valor_total,

            id_funcionario_aprovador = p_id_funcionario
        WHERE id_emprestimo = p_id_emprestimo
          AND status = 'PENDENTE';

    ELSE
        UPDATE emprestimo
        SET status = 'REJEITADO',
            data_aprovacao = CURRENT_TIMESTAMP,

            id_funcionario_aprovador = p_id_funcionario
        WHERE id_emprestimo = p_id_emprestimo
          AND status = 'PENDENTE';
    END IF;

    -- Auditoria
    PERFORM fn_registrar_auditoria(
        p_id_funcionario,
        'DECISAO_EMPRESTIMO', 
        CONCAT('Empréstimo ', p_id_emprestimo, ' => ',
               CASE WHEN p_aprovado THEN 'APROVADO' ELSE 'REJEITADO' END)
    );
END;
$$;

CREATE INDEX idx_emprestimo_cliente_data ON emprestimo (id_cliente, data_solicitacao);
CREATE INDEX idx_transacao_conta_data ON transacao(id_conta_origem, data_hora DESC);
CREATE INDEX idx_emprestimo_aprovado ON emprestimo (id_cliente, data_solicitacao) WHERE status = 'APROVADO';

CREATE UNIQUE INDEX idx_usuario_cpf ON usuario(cpf);
CREATE UNIQUE INDEX idx_conta_numero ON conta(numero_conta);

CREATE INDEX idx_emprestimo_status ON emprestimo(status);
CREATE INDEX idx_solicitacao_conta_status ON solicitacao_conta(status);
CREATE INDEX idx_funcionario_id_agencia ON funcionario(id_agencia);

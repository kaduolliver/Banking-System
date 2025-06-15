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

        -- 1. Atualiza o saldo da conta do cliente diretamente
        UPDATE conta
        SET saldo = saldo + NEW.valor_solicitado
        WHERE id_conta = NEW.id_conta;

        -- 2. Registra a transação de depósito na tabela de transações para auditoria
        INSERT INTO transacao (
            id_conta_origem, -- Para um depósito de empréstimo, a conta do cliente é a destino.
                             -- Usaremos id_conta_origem como a conta que recebeu o depósito
                             -- e id_conta_destino como NULL, já que o "origem" é o próprio banco.
            tipo_transacao,
            valor,
            data_hora,
            descricao
        ) VALUES (
            NEW.id_conta,
            'deposito',
            NEW.valor_solicitado,
            CURRENT_TIMESTAMP,
            CONCAT('Depósito de Empréstimo ID ', NEW.id_emprestimo, ' aprovado.')
        );

        -- Opcional: Registrar na auditoria que um empréstimo foi aprovado e depositado
        PERFORM fn_registrar_auditoria(
            NULL, -- ou o ID do funcionário que aprovou, se tiver acesso aqui
            'EMPRESTIMO_DEPOSITADO',
            CONCAT('Empréstimo ID ', NEW.id_emprestimo, ' de R$', NEW.valor_solicitado, ' depositado na conta ID ', NEW.id_conta)
        );

    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Função para atualizar o saldo depois de depositar/sacar/transferir (emprestimo)
CREATE OR REPLACE FUNCTION fn_atualizar_saldo_conta()
RETURNS TRIGGER AS $$
DECLARE
    v_tipo_conta    TEXT;
    v_saldo         NUMERIC(15,2);
    v_limite        NUMERIC(15,2) := 0;
    v_total_depositos_hoje NUMERIC(15,2); -- Nova variável para o total de depósitos
    LIMITE_DEPOSITO_DIARIO NUMERIC(15,2) := 10000.00; -- Constante para o limite

BEGIN
    -- 1. Recupera saldo e, se for corrente, o limite
    SELECT c.tipo_conta,
           c.saldo,
           COALESCE(cc.limite, 0)
    INTO   v_tipo_conta,
           v_saldo,
           v_limite
    FROM   conta c
    LEFT JOIN conta_corrente cc USING (id_conta)
    WHERE  c.id_conta = NEW.id_conta_origem;

    -- 2. Valida saldo disponível (existente)
    IF NEW.tipo_transacao IN ('saque', 'transferencia') THEN
        IF (v_saldo + CASE WHEN v_tipo_conta = 'corrente' THEN v_limite ELSE 0 END) < NEW.valor THEN
            RAISE EXCEPTION 'Saldo (incluindo limite) insuficiente na conta de origem.';
        END IF;
    END IF;

    -- 3. **NOVA LÓGICA: Verificar limite diário para depósitos**
    IF NEW.tipo_transacao = 'deposito' THEN
        -- Calcula o total de depósitos feitos na conta_origem HOJE
        SELECT COALESCE(SUM(valor), 0)
        INTO v_total_depositos_hoje
        FROM transacao
        WHERE id_conta_origem = NEW.id_conta_origem
          AND tipo_transacao = 'deposito'
          AND data_hora::DATE = CURRENT_DATE;

        -- Se a soma dos depósitos de hoje mais o novo depósito exceder o limite
        IF (v_total_depositos_hoje + NEW.valor) > LIMITE_DEPOSITO_DIARIO THEN
            RAISE EXCEPTION 'Limite de depósito diário de R$ % atingido para esta conta. Total depositado hoje: R$ %. Depósito atual: R$ %.',
                            LIMITE_DEPOSITO_DIARIO, v_total_depositos_hoje, NEW.valor;
        END IF;
    END IF;

    -- 4. Atualiza saldo (existente)
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


-- Função de debitar
CREATE OR REPLACE FUNCTION fn_debitar_saldo_saque()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.tipo_transacao = 'saque' THEN
    UPDATE conta
    SET saldo = saldo - NEW.valor
    WHERE id_conta = NEW.id_conta_origem;
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
BEGIN
    IF NEW.status = 'APROVADO' AND (OLD.status IS DISTINCT FROM 'APROVADO') THEN
        -- Construir base do número da conta
        v_numero_base := TO_CHAR(NOW(), 'YYYYMMDDHH24MISS') || NEW.id_solicitacao;

        -- Calcular dígito verificador (DV) com módulo 10
        FOR i IN 1..LENGTH(v_numero_base) LOOP
            v_char := SUBSTRING(v_numero_base FROM i FOR 1);
            IF v_char ~ '[0-9]' THEN
                v_digit := CAST(v_char AS INT);
                v_soma := v_soma + v_digit;
            END IF;
        END LOOP;

        v_dv := v_soma % 10;

        -- Gerar número final da conta com DV
        v_numero_conta := 'BR' || v_numero_base || v_dv;

        -- Buscar o ID da agência do funcionário aprovador
        SELECT f.id_agencia INTO v_id_agencia
        FROM funcionario f
        WHERE f.id_funcionario = NEW.id_funcionario_aprovador;

        IF v_id_agencia IS NULL THEN
            RAISE EXCEPTION 'Agência do funcionário aprovador (ID: %) não encontrada.', NEW.id_funcionario_aprovador;
        END IF;

        -- Inserir conta
        INSERT INTO conta (
            numero_conta, id_agencia, saldo, tipo_conta, id_cliente, data_abertura, status
        ) VALUES (
            v_numero_conta, v_id_agencia, COALESCE(NEW.valor_inicial, 0.00),
            NEW.tipo_conta, NEW.id_cliente, CURRENT_DATE, 'ativa'
        )
        RETURNING id_conta INTO v_id_nova_conta;

        -- Inserir dados específicos conforme tipo da conta
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
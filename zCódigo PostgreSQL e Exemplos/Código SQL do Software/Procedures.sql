-- Procedure processar_emprestimo
CREATE OR REPLACE PROCEDURE processar_emprestimo(
    IN p_id_cliente     INT,
    IN p_id_conta       INT,
    IN p_valor          NUMERIC(15,2),
    IN p_prazo          INT,
    IN p_finalidade     VARCHAR(100),
    IN p_score_risco    NUMERIC(5,2)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_status          VARCHAR(20) := 'PENDENTE';      
    v_taxa            NUMERIC(5,2) := 0;
    v_valor_total     NUMERIC(15,2) := p_valor;
BEGIN
    -- Aprovação automática apenas se score for MUITO alto (exemplo ≥ 80)
    IF p_score_risco >= 80 THEN
        v_status := 'APROVADO';
        v_taxa   := 0.5;                               -- calcule como quiser
        v_valor_total := p_valor * POWER(1 + v_taxa/100, p_prazo);

		-- Rejeição automática
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
    IN p_aprovado      BOOLEAN,
    IN p_id_funcionario INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_score       NUMERIC(5,2);
    v_taxa        NUMERIC(5,2) := 0;
    v_valor       NUMERIC(15,2);
    v_valor_total NUMERIC(15,2);
    v_prazo       INT;
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
        SET status              = 'APROVADO',
            data_aprovacao      = CURRENT_TIMESTAMP,
            taxa_juros_mensal   = v_taxa,
            valor_total         = v_valor_total
        WHERE id_emprestimo = p_id_emprestimo
          AND status = 'PENDENTE';

    ELSE
        UPDATE emprestimo
        SET status         = 'REJEITADO',
            data_aprovacao = CURRENT_TIMESTAMP
        WHERE id_emprestimo = p_id_emprestimo
          AND status = 'PENDENTE';
    END IF;

    -- Auditoria
    PERFORM fn_registrar_auditoria(
        p_id_funcionario,
        'DECISAO EMPRESTIMO',
        CONCAT('Empréstimo ', p_id_emprestimo, ' => ',
               CASE WHEN p_aprovado THEN 'APROVADO' ELSE 'REJEITADO' END)
    );
END;
$$;
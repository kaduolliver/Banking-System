-- Trigger para empréstimo
CREATE OR TRIGGER depositar_emprestimo_trigger
AFTER INSERT OR UPDATE ON emprestimo
FOR EACH ROW
EXECUTE FUNCTION fn_depositar_emprestimo_na_conta();

-- Trigger para atualizar saldo
CREATE TRIGGER tg_atualizar_saldo_conta
BEFORE INSERT ON transacao
FOR EACH ROW
EXECUTE FUNCTION fn_atualizar_saldo_conta();

-- Trigger de debitar
CREATE TRIGGER trg_debitar_saldo_saque
AFTER INSERT ON transacao
FOR EACH ROW
EXECUTE FUNCTION fn_debitar_saldo_saque();

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

CREATE TRIGGER trigger_gerar_codigo_funcionario_update
BEFORE UPDATE ON funcionario
FOR EACH ROW
WHEN (
    NEW.codigo_funcionario IS DISTINCT FROM OLD.codigo_funcionario AND
    NEW.cargo <> OLD.cargo
)
EXECUTE FUNCTION gerar_codigo_funcionario();
-- Resetar tabelas do banco de dados

TRUNCATE TABLE conta_poupanca, conta_corrente, conta_investimento, transacao, emprestimo,
               relatorio, solicitacao_conta, auditoria, conta, agencia, endereco,
               funcionario, cliente, usuario RESTART IDENTITY;

-- Mudar tipo_usuario 

BEGIN;

-- 1. Remover o usuário da tabela funcionario
DELETE FROM funcionario
WHERE id_usuario = (SELECT id_usuario FROM usuario WHERE cpf = '44444444444'); -- Substitua pelo CPF real

-- 2. Inserir o usuário na tabela cliente
INSERT INTO cliente (id_usuario, score_credito)
VALUES ((SELECT id_usuario FROM usuario WHERE cpf = '44444444444'), 50); -- Substitua pelo CPF real e score inicial

-- 3. Atualizar o tipo_usuario na tabela usuario
UPDATE usuario
SET tipo_usuario = 'cliente'
WHERE cpf = '44444444444'; -- Substitua pelo CPF real

COMMIT;


-- Mudar score_credito do cliente

UPDATE cliente
SET score_credito = 95 -- Determine o score aqui. Emprestimo -> if score_credito >= 80 else "REJEITADO"
WHERE id_cliente = 1; -- Substitua 1 pelo id_cliente do cliente

-- Mudar limite da conta corrente:

UPDATE conta_corrente
SET limite = 5000.00
WHERE id_conta_corrente = 1;

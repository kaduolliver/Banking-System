-- Resetar banco de dados

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
VALUES ((SELECT id_usuario FROM usuario WHERE cpf = '44444444444'), 0); -- Substitua pelo CPF real e score inicial

-- 3. Atualizar o tipo_usuario na tabela usuario
UPDATE usuario
SET tipo_usuario = 'cliente'
WHERE cpf = '44444444444'; -- Substitua pelo CPF real

COMMIT;

-- Inserir hierarquia

-- Admin

UPDATE funcionario
SET codigo_funcionario = 'ADM001',
    cargo = 'Admin',
    nivel_hierarquico = 3,
    id_supervisor = NULL -- NULL porque admin não tem supervisor
WHERE id_usuario = 1; -- quem será o admin

-- Gerente

UPDATE funcionario
SET codigo_funcionario = 'GER001',
    cargo = 'Gerente',
    nivel_hierarquico = 2,
    id_supervisor = 1 -- id_usuario do supervisor [Admin]
WHERE id_usuario = 2; -- quem será o gerente

-- Estagiário

UPDATE funcionario
SET codigo_funcionario = 'EST001',
    cargo = 'Estagiário',
    nivel_hierarquico = 1,
    id_supervisor = 2 -- id_usuario do supervisor [Gerente]
WHERE id_usuario = 3; -- quem será o estagiário

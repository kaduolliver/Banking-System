CREATE INDEX idx_emprestimo_cliente_data ON emprestimo (id_cliente, data_solicitacao);
CREATE INDEX idx_transacao_conta_data ON transacao(id_conta_origem, data_hora DESC);
CREATE INDEX idx_emprestimo_aprovado ON emprestimo (id_cliente, data_solicitacao) WHERE status = 'APROVADO';

CREATE UNIQUE INDEX idx_usuario_cpf ON usuario(cpf);
CREATE UNIQUE INDEX idx_conta_numero ON conta(numero_conta);

CREATE INDEX idx_emprestimo_status ON emprestimo(status);
CREATE INDEX idx_solicitacao_conta_status ON solicitacao_conta(status);
CREATE INDEX idx_funcionario_id_agencia ON funcionario(id_agencia);
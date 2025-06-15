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

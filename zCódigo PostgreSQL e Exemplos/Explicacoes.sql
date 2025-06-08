-- Abordagem 1: Usando a coluna cargo na tabela funcionario com uma ordem definida

-- Esta � a abordagem mais simples e que voc� j� tem em parte com sua tabela funcionario. Voc� pode adicionar uma coluna para definir a hierarquia, por exemplo, um n�vel num�rico ou uma ordem expl�cita dos cargos.

-- Modifica��o na Tabela funcionario:

-- Voc� j� tem a coluna cargo VARCHAR(100) NOT NULL. Podemos aproveitar isso e, opcionalmente, adicionar uma coluna para definir a "ordem" ou "n�vel" hier�rquico, se voc� precisar de uma ordena��o expl�cita que n�o seja alfab�tica pelo nome do cargo.


-- ALTERA��O DA TABELA FUNCIONARIO
ALTER TABLE funcionario
ADD COLUMN nivel_hierarquico INT; -- Opcional, para uma ordem num�rica da hierarquia

-- Adiciona uma restri��o CHECK para os cargos permitidos, se n�o quiser que o cargo_usuario na tabela "usuario" seja o �nico ponto de verdade
ALTER TABLE funcionario
ADD CONSTRAINT check_cargo_funcionario CHECK (cargo IN ('Estagi�rio', 'Gerente', 'Admin'));

-- Exemplo de atualiza��o para definir o n�vel hier�rquico
UPDATE funcionario SET nivel_hierarquico = 1 WHERE cargo = 'Estagi�rio';
UPDATE funcionario SET nivel_hierarquico = 2 WHERE cargo = 'Gerente';
UPDATE funcionario SET nivel_hierarquico = 3 WHERE cargo = 'Admin';


-- Como cadastrar a hierarquia (exemplo de inser��o):

-- Supondo que voc� j� tenha usu�rios cadastrados na tabela 'usuario'

-- Inserir um Admin (n�vel mais alto)
INSERT INTO funcionario (id_usuario, codigo_funcionario, cargo, nivel_hierarquico, id_supervisor)
VALUES (101, 'ADM001', 'Admin', 3, NULL); -- Admin n�o tem supervisor

-- Inserir um Gerente (supervisionado pelo Admin)
INSERT INTO funcionario (id_usuario, codigo_funcionario, cargo, nivel_hierarquico, id_supervisor)
VALUES (102, 'GER001', 'Gerente', 2, (SELECT id_funcionario FROM funcionario WHERE codigo_funcionario = 'ADM001'));

-- Inserir um Estagi�rio (supervisionado pelo Gerente)
INSERT INTO funcionario (id_usuario, codigo_funcionario, cargo, nivel_hierarquico, id_supervisor)
VALUES (103, 'EST001', 'Estagi�rio', 1, (SELECT id_funcionario FROM funcionario WHERE codigo_funcionario = 'GER001'));

-- Abordagem 2: Usando a coluna tipo_usuario na tabela usuario para pap�is de sistema e a tabela funcionario para pap�is espec�ficos da empresa.
-- Voc� j� tem tipo_usuario VARCHAR(50) NOT NULL CHECK (tipo_usuario IN ('cliente', 'funcionario')) na tabela usuario. Esta � uma distin��o importante para o n�vel mais alto de acesso � aplica��o (se � um usu�rio geral ou um funcion�rio).

-- Para a hierarquia interna de funcion�rios (Estagi�rio, Gerente, Admin), a tabela funcionario � o local correto.

-- Esquema atual (e que est� bom):

-- usuario: Define quem pode logar no sistema (id_usuario, nome, tipo_usuario (cliente/funcionario), senha_hash, etc.)
-- funcionario: Complementa as informa��es de um usuario que � do tipo 'funcionario', adicionando detalhes espec�ficos da fun��o (cargo, c�digo do funcion�rio, supervisor, etc.).
-- Esta separa��o � interessante porque um usuario pode ser um funcion�rio hoje e amanh� n�o ser mais (ou se tornar um cliente), sem perder seu registro de usu�rio.

-- Como funciona a hierarquia com seu esquema atual:

-- A hierarquia � primariamente definida pelo campo cargo na tabela funcionario e pela auto-refer�ncia id_supervisor. A coluna tipo_usuario na tabela usuario serve para uma categoriza��o mais ampla de usuario (cliente ou funcion�rio), o que � �til para controle de acesso em um n�vel mais geral na aplica��o.

-- Voc� pode usar o campo cargo para diferenciar os tr�s n�veis: 'Estagi�rio', 'Gerente', 'Admin'.

-- Vantagens dessa abordagem:

-- Clareza: A fun��o interna do funcion�rio � bem definida em funcionario.cargo.
-- Flexibilidade: Se os cargos mudarem, voc� s� precisa atualizar os dados na tabela funcionario.
-- Integridade: As restri��es CHECK garantem que apenas cargos v�lidos sejam inseridos.
-- Hierarquia de Supervis�o: A coluna id_supervisor permite construir a cadeia de comando.
-- Como as duas se complementam para controle de acesso (RBAC - Role-Based Access Control)
-- Para uma aplica��o financeira, voc� provavelmente precisa de um sistema de controle de acesso baseado em pap�is (RBAC).

-- Pap�is no n�vel de aplica��o (via tipo_usuario):

-- cliente: Acessa funcionalidades como ver extrato, fazer transa��es, solicitar empr�stimos.
-- funcionario: Acessa funcionalidades administrativas (gerenciar contas, aprovar empr�stimos, etc.).
-- Hierarquia de permiss�es dentro do papel funcionario (via funcionario.cargo):

-- Estagi�rio: Permiss�es mais limitadas (e.g., visualiza��o, entrada de dados b�sica).
-- Gerente: Permiss�es intermedi�rias (e.g., aprovar algumas opera��es, visualizar relat�rios completos).
-- Admin: Permiss�es mais amplas (e.g., aprovar tudo, gerenciar usu�rios, configurar sistema).
-- Implementa��o de RBAC no c�digo da aplica��o:

-- No seu c�digo Python (ou na linguagem que estiver usando), ao autenticar um usu�rio:

-- Voc� verifica o usuario.tipo_usuario. Se for 'funcionario', voc� continua.
-- Ent�o, voc� consulta a tabela funcionario para obter o cargo desse funcion�rio.
-- Com base no cargo (Estagi�rio, Gerente, Admin), voc� aplica as regras de neg�cio e de interface para controlar o que o funcion�rio pode ver e fazer. Por exemplo:

if funcionario.cargo == 'Admin':
    # Mostrar todas as op��es de gerenciamento
elif funcionario.cargo == 'Gerente':
    # Mostrar op��es de gerenciamento espec�ficas de gerente
elif funcionario.cargo == 'Estagi�rio':
    # Mostrar op��es limitadas
-- Abordagem 1: Usando a coluna cargo na tabela funcionario com uma ordem definida

-- Esta é a abordagem mais simples e que você já tem em parte com sua tabela funcionario. Você pode adicionar uma coluna para definir a hierarquia, por exemplo, um nível numérico ou uma ordem explícita dos cargos.

-- Modificação na Tabela funcionario:

-- Você já tem a coluna cargo VARCHAR(100) NOT NULL. Podemos aproveitar isso e, opcionalmente, adicionar uma coluna para definir a "ordem" ou "nível" hierárquico, se você precisar de uma ordenação explícita que não seja alfabética pelo nome do cargo.


-- ALTERAÇÃO DA TABELA FUNCIONARIO
ALTER TABLE funcionario
ADD COLUMN nivel_hierarquico INT; -- Opcional, para uma ordem numérica da hierarquia

-- Adiciona uma restrição CHECK para os cargos permitidos, se não quiser que o cargo_usuario na tabela "usuario" seja o único ponto de verdade
ALTER TABLE funcionario
ADD CONSTRAINT check_cargo_funcionario CHECK (cargo IN ('Estagiário', 'Gerente', 'Admin'));

-- Exemplo de atualização para definir o nível hierárquico
UPDATE funcionario SET nivel_hierarquico = 1 WHERE cargo = 'Estagiário';
UPDATE funcionario SET nivel_hierarquico = 2 WHERE cargo = 'Gerente';
UPDATE funcionario SET nivel_hierarquico = 3 WHERE cargo = 'Admin';


-- Como cadastrar a hierarquia (exemplo de inserção):

-- Supondo que você já tenha usuários cadastrados na tabela 'usuario'

-- Inserir um Admin (nível mais alto)
INSERT INTO funcionario (id_usuario, codigo_funcionario, cargo, nivel_hierarquico, id_supervisor)
VALUES (101, 'ADM001', 'Admin', 3, NULL); -- Admin não tem supervisor

-- Inserir um Gerente (supervisionado pelo Admin)
INSERT INTO funcionario (id_usuario, codigo_funcionario, cargo, nivel_hierarquico, id_supervisor)
VALUES (102, 'GER001', 'Gerente', 2, (SELECT id_funcionario FROM funcionario WHERE codigo_funcionario = 'ADM001'));

-- Inserir um Estagiário (supervisionado pelo Gerente)
INSERT INTO funcionario (id_usuario, codigo_funcionario, cargo, nivel_hierarquico, id_supervisor)
VALUES (103, 'EST001', 'Estagiário', 1, (SELECT id_funcionario FROM funcionario WHERE codigo_funcionario = 'GER001'));

-- Abordagem 2: Usando a coluna tipo_usuario na tabela usuario para papéis de sistema e a tabela funcionario para papéis específicos da empresa.
-- Você já tem tipo_usuario VARCHAR(50) NOT NULL CHECK (tipo_usuario IN ('cliente', 'funcionario')) na tabela usuario. Esta é uma distinção importante para o nível mais alto de acesso à aplicação (se é um usuário geral ou um funcionário).

-- Para a hierarquia interna de funcionários (Estagiário, Gerente, Admin), a tabela funcionario é o local correto.

-- Esquema atual (e que está bom):

-- usuario: Define quem pode logar no sistema (id_usuario, nome, tipo_usuario (cliente/funcionário), senha_hash, etc.)
-- funcionario: Complementa as informações de um usuário que é do tipo 'funcionário', adicionando detalhes específicos da função (cargo, código do funcionário, supervisor, etc.).
-- Esta separação é interessante porque um usuário pode ser um funcionário hoje e amanhã não ser mais (ou se tornar um cliente), sem perder seu registro de usuário.

-- Como funciona a hierarquia com seu esquema atual:

-- A hierarquia é primariamente definida pelo campo cargo na tabela funcionario e pela auto-referência id_supervisor. A coluna tipo_usuario na tabela usuario serve para uma categorização mais ampla de usuário (cliente ou funcionário), o que é útil para controle de acesso em um nível mais geral na aplicação.

-- Você pode usar o campo cargo para diferenciar os três níveis: 'Estagiário', 'Gerente', 'Admin'.

-- Vantagens dessa abordagem:

-- Clareza: A função interna do funcionário é bem definida em funcionario.cargo.
-- Flexibilidade: Se os cargos mudarem, você só precisa atualizar os dados na tabela funcionario.
-- Integridade: As restrições CHECK garantem que apenas cargos válidos sejam inseridos.
-- Hierarquia de Supervisão: A coluna id_supervisor permite construir a cadeia de comando.

-- Como as duas se complementam para controle de acesso (RBAC - Role-Based Access Control):

-- Para uma aplicação financeira, você provavelmente precisa de um sistema de controle de acesso baseado em papéis (RBAC).

-- Papéis no nível de aplicação (via tipo_usuario):

-- cliente: Acessa funcionalidades como ver extrato, fazer transações, solicitar empréstimos.
-- funcionário: Acessa funcionalidades administrativas (gerenciar contas, aprovar empréstimos, etc.).

-- Hierarquia de permissões dentro do papel funcionário (via funcionario.cargo):

-- Estagiário: Permissões mais limitadas (ex.: visualização, entrada de dados básica).
-- Gerente: Permissões intermediárias (ex.: aprovar algumas operações, visualizar relatórios completos).
-- Admin: Permissões mais amplas (ex.: aprovar tudo, gerenciar usuários, configurar sistema).

-- Implementação de RBAC no código da aplicação:

-- No seu código Python (ou na linguagem que estiver usando), ao autenticar um usuário:

-- Você verifica o usuario.tipo_usuario. Se for 'funcionário', você continua.
-- Então, você consulta a tabela funcionario para obter o cargo desse funcionário.
-- Com base no cargo (Estagiário, Gerente, Admin), você aplica as regras de negócio e de interface para controlar o que o funcionário pode ver e fazer. Por exemplo:

if funcionario.cargo == 'Admin':
    # Mostrar todas as opções de gerenciamento
elif funcionario.cargo == 'Gerente':
    # Mostrar opções de gerenciamento específicas de gerente
elif funcionario.cargo == 'Estagiário':
    # Mostrar opções limitadas

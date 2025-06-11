import { useState, useEffect } from 'react';

export default function ManagerConfig() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        // Em uma aplicação real, você buscaria os dados da sua API,
        // que já incluiria a coluna 'inativo' (ou 'ativo') do banco de dados.
        // const response = await fetch('/api/employees');
        // if (!response.ok) {
        //   throw new Error('Erro ao buscar funcionários');
        // }
        // const data = await response.json();
        // setEmployees(data);

        // Dados simulados para demonstração, com a propriedade 'inativo'
        setTimeout(() => {
          setEmployees([
            { id: 1, nome: 'João Silva', cargo: 'Gerente', codigo_funcionario: 'GER001', inativo: false },
            { id: 2, nome: 'Maria Oliveira', cargo: 'Analista', codigo_funcionario: 'ANL005', inativo: false },
            { id: 3, nome: 'Carlos Souza', cargo: 'Estagiário', codigo_funcionario: 'EST012', inativo: true }, // Exemplo de funcionário inativo
            { id: 4, nome: 'Ana Costa', cargo: 'Coordenador', codigo_funcionario: 'COO002', inativo: false },
            { id: 5, nome: 'Pedro Almeida', cargo: 'Analista Financeiro', codigo_funcionario: 'ANL006', inativo: false },
            { id: 6, nome: 'Sofia Santos', cargo: 'Recursos Humanos', codigo_funcionario: 'RH001', inativo: true }, // Outro inativo
            { id: 7, nome: 'Lucas Fernandes', cargo: 'Desenvolvedor', codigo_funcionario: 'DEV003', inativo: false },
            { id: 8, nome: 'Isabela Pereira', cargo: 'Estagiária', codigo_funcionario: 'EST013', inativo: false },
          ]);
          setLoading(false);
        }, 100);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchEmployees();
  }, []);

  const toggleStatus = async (id) => {
    // Atualiza o estado no frontend imediatamente para dar um feedback visual rápido
    setEmployees(prevEmployees =>
      prevEmployees.map(employee =>
        employee.id === id ? { ...employee, inativo: !employee.inativo } : employee
      )
    );

    // Em uma aplicação real, você enviaria uma requisição para sua API aqui
    // para atualizar o status no banco de dados.
    // Exemplo:
    // try {
    //   const employeeToUpdate = employees.find(emp => emp.id === id);
    //   const newStatus = !employeeToUpdate.inativo;
    //   const response = await fetch(`/api/employees/${id}/status`, {
    //     method: 'PUT', // ou 'PATCH'
    //     headers: {
    //       'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify({ inativo: newStatus }),
    //   });
    //   if (!response.ok) {
    //     // Se a atualização falhar no backend, você pode reverter o estado no frontend
    //     throw new Error('Falha ao atualizar status no servidor');
    //   }
    //   // Opcional: recarregar funcionários ou fazer algo mais após o sucesso
    // } catch (err) {
    //   console.error("Erro ao atualizar status:", err);
    //   setError(err.message);
    //   // Reverte o estado no frontend se houver erro
    //   setEmployees(prevEmployees =>
    //     prevEmployees.map(employee =>
    //       employee.id === id ? { ...employee, inativo: !employee.inativo } : employee
    //     )
    //   );
    // }
  };

  if (loading) {
    return <div className="text-gray-300">Carregando funcionários...</div>;
  }

  if (error) {
    return <div className="text-red-500">Erro: {error}</div>;
  }

  return (
    <div className="p-6 shadow-lg h-full flex flex-col">
      <h2 className="text-2xl font-bold text-white mb-6">Gerenciamento de Funcionários</h2>

      {employees.length === 0 ? (
        <p className="text-gray-400">Nenhum funcionário encontrado.</p>
      ) : (
        <div className="overflow-y-auto flex-grow rounded-lg">
          <table className="min-w-full bg-zinc-900 rounded-lg">
            <thead>
              <tr className="bg-black text-left text-gray-200 uppercase text-sm leading-normal">
                <th className="py-3 px-6 text-left">Nome do Funcionário</th>
                <th className="py-3 px-6 text-left">Cargo</th>
                <th className="py-3 px-6 text-left">Código do Funcionário</th>
                <th className="py-3 px-6 text-center">Status</th> {/* Nova coluna para o status */}
              </tr>
            </thead>
            <tbody className="text-zinc-300 text-sm font-light">
              {employees.map((employee) => (
                <tr key={employee.id} className="border-b border-zinc-600 hover:bg-zinc-600">
                  <td className="py-3 px-6 text-left whitespace-nowrap">{employee.nome}</td>
                  <td className="py-3 px-6 text-left">{employee.cargo}</td>
                  <td className="py-3 px-6 text-left">{employee.codigo_funcionario}</td>
                  <td className="py-3 px-6 text-center">
                    <button
                      onClick={() => toggleStatus(employee.id)}
                      className={`
                        font-bold py-1 px-3 rounded text-xs transition-colors duration-200
                        ${
                          employee.inativo
                            ? 'bg-red-600 hover:bg-red-700 text-white'
                            : 'bg-green-600 hover:bg-green-700 text-white'
                        }
                      `}
                    >
                      {employee.inativo ? 'Inativo' : 'Ativo'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
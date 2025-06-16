export async function buscarFuncionarios() {
  const response = await fetch('http://localhost:5000/api/employees', {
    credentials: 'include'
  });
  if (!response.ok) {
    throw new Error('Erro ao buscar funcionários');
  }
  return response.json();
}

export async function atualizarFuncionariosStatus(id, inativo) {
  const response = await fetch(`http://localhost:5000/api/employees/${id}/status`, {
    credentials: 'include',
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ inativo }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || 'Falha ao atualizar status do funcionário');
  }
}

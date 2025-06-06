export async function atualizarTelefone(telefone) {
  const response = await fetch('http://localhost:5000/api/usuario/atualizar', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ telefone }),
    credentials: 'include',
  });

  if (!response.ok) {
    try {
      const data = await response.json();
      throw new Error(data.erro || 'Erro ao atualizar telefone');
    } catch {
      throw new Error('Erro ao atualizar telefone');
    }
  }

  return response.json();
}

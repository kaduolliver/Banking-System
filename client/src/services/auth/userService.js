export async function atualizarTelefone(telefone) {
  const response = await fetch('/api/usuario/atualizar', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ telefone }),
  });

  if (!response.ok) {
    const data = await response.json();
    throw new Error(data.erro || 'Erro ao atualizar telefone');
  }

  return response.json();
}

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

export async function enviarEndereco(dadosEndereco) {
  try {
    const response = await fetch('http://localhost:5000/api/usuario/endereco', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(dadosEndereco),
      credentials: 'include'
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.erro || 'Erro desconhecido');
    }

    console.log(data.mensagem);
    return data;
  } catch (error) {
    console.error('Erro ao enviar endereço:', error.message);
    throw error;
  }
}

export async function buscarEndereco() {
  try {
    const response = await fetch('http://localhost:5000/api/usuario/endereco', {
      method: 'GET',
      credentials: 'include',
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.erro || 'Erro desconhecido');
    }

    return data;
    
  } catch (error) {
    console.error('Erro ao buscar endereço:', error.message);
    throw error;
  }
}

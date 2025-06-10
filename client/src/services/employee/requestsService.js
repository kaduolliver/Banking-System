export async function getSolicitacoesPendentes() {
  try {
    const res = await fetch('http://localhost:5000/api/solicitacoes/pendentes', {
      credentials: 'include',
    });

    const contentType = res.headers.get('content-type');

    if (!res.ok) {
      const text = await res.text();
      console.error('Erro de resposta:', text);
      throw new Error('Erro ao buscar solicitações.');
    }

    if (contentType && contentType.includes('application/json')) {
      return await res.json();
    } else {
      const text = await res.text();
      console.error('Resposta não JSON recebida:', text);
      throw new Error('Resposta do servidor não está em formato JSON.');
    }
  } catch (error) {
    console.error(error);
    throw error;
  }
}


export async function aprovarSolicitacao(id) {
  try {
    const res = await fetch(`http://localhost:5000/api/solicitacoes/${id}/aprovar`, {
      method: 'POST',
      credentials: 'include',
    });
    if (!res.ok) throw new Error('Erro ao aprovar solicitação.');
    return await res.json();
  } catch (error) {
    console.error(error);
    throw error;
  }
}

export async function rejeitarSolicitacao(id) {
  try {
    const res = await fetch(`http://localhost:5000/api/solicitacoes/${id}/rejeitar`, {
      method: 'POST',
      credentials: 'include',
    });
    if (!res.ok) throw new Error('Erro ao rejeitar solicitação.');
    return await res.json();
  } catch (error) {
    console.error(error);
    throw error;
  }
}

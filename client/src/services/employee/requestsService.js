
// Solicitações para abertura de conta
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

export async function aprovarSolicitacaoConta(id) {
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

export async function rejeitarSolicitacaoConta(id) {
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

// ----------------------------------------------------------------------------------------


// Requisições para solicitações de empréstimos manuais
async function handleResponse(res) {
  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    
    const erroMsg = data?.erro || res.statusText;
    throw new Error(erroMsg);
  }
  return data;
}

export async function getSolicitacoesEmprestimosPendentes() {
  const res = await fetch(`http://localhost:5000/api/emprestimos/pendentes`, {
    method: 'GET',
    credentials: 'include',
  });
  return handleResponse(res);
}

async function decidirSolicitacaoEmprestimo(id, aprovado) {
  const res = await fetch(`http://localhost:5000/api/emprestimos/${id}/decidir`, {
    method: 'PUT',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ aprovado }),
  });
  return handleResponse(res);
}

export function aprovarSolicitacaoEmprestimo(id) {
  return decidirSolicitacaoEmprestimo(id, true);
}

export function rejeitarSolicitacaoEmprestimo(id) {
  return decidirSolicitacaoEmprestimo(id, false);
}

// ----------------------------------------------------------------------------------------
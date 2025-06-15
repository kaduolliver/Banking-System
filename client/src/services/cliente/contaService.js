export async function verificarConta(clienteId) {
  if (!clienteId) throw new Error("ID do cliente não fornecido");

  const response = await fetch(`http://localhost:5000/api/cliente/${clienteId}/conta`, {
    credentials: 'include',
  });
  if (!response.ok) throw new Error("Erro ao verificar conta");

  const data = await response.json();
  return data;
}

export async function solicitarAberturaConta(clienteId, tipoConta) {
  if (!clienteId) throw new Error("ID do cliente não fornecido");
  if (!tipoConta) throw new Error("Tipo de conta não informado");

  const response = await fetch(`http://localhost:5000/api/solicitacoes`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: 'include',
    body: JSON.stringify({
      cliente_id: clienteId,
      tipo_conta: tipoConta,  
    }),
  });

  if (!response.ok) {
    const erro = await response.json();
    throw new Error(erro?.erro || "Erro ao enviar solicitação");
  }
}

export const solicitarEmprestimo = async (dadosEmprestimo) => {
  
  const response = await fetch('http://localhost:5000/api/emprestimos', {
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json',
      
    },
    credentials: 'include',
    body: JSON.stringify(dadosEmprestimo), 
  });

 
  if (!response.ok) {
    const errorData = await response.json(); 
    
    throw new Error(errorData.erro || 'Erro ao solicitar empréstimo.');
  }

  
  return response.json();
};

export async function realizarSaque({ id_conta, numero_conta, valor, descricao }) {
  if (!id_conta && !numero_conta) throw new Error("Informe 'id_conta' ou 'numero_conta' para saque.");
  if (!valor) throw new Error("Valor para saque não informado.");

  const body = { valor };
  if (id_conta) body.id_conta = id_conta;
  if (numero_conta) body.numero_conta = numero_conta;
  if (descricao) body.descricao = descricao;

  const response = await fetch('http://localhost:5000/api/saque', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.erro || 'Erro ao realizar saque.');
  }

  return response.json();
}

export async function realizarDeposito({ id_conta, numero_conta, valor, descricao }) {
  if (!id_conta && !numero_conta)
    throw new Error("Informe 'id_conta' ou 'numero_conta' para depósito.");
  if (!valor) throw new Error("Valor para depósito não informado.");

  const body = { valor };
  if (id_conta) body.id_conta = id_conta;
  if (numero_conta) body.numero_conta = numero_conta;
  if (descricao) body.descricao = descricao;

  const response = await fetch('http://localhost:5000/api/deposito', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.erro || 'Erro ao realizar depósito.');
  }

  return response.json();
}

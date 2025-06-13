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

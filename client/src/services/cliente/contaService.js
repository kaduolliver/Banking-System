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
  // Faz uma requisição POST para o endpoint de empréstimos
  const response = await fetch('http://localhost:5000/api/emprestimos', {
    method: 'POST', // Define o método da requisição como POST
    headers: {
      'Content-Type': 'application/json',
       // Informa que o corpo da requisição é JSON
    },
    credentials: 'include',
    body: JSON.stringify(dadosEmprestimo), // Converte o objeto JavaScript para uma string JSON
  });

  // Verifica se a resposta da requisição foi bem-sucedida (status 2xx)
  if (!response.ok) {
    const errorData = await response.json(); // Tenta parsear o erro do JSON
    // Lança um erro com a mensagem do backend ou uma mensagem genérica
    throw new Error(errorData.erro || 'Erro ao solicitar empréstimo.');
  }

  // Se a resposta for OK, retorna os dados da resposta (geralmente uma mensagem de sucesso)
  return response.json();
};

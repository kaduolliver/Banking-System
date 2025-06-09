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

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.erro || 'Erro desconhecido');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao buscar endereço:', error.message);
    throw error;
  }
}

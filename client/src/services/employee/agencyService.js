export async function enviarEnderecoAgencia(dadosEndereco) {
    try {
        const response = await fetch('http://localhost:5000/api/agencia/endereco', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dadosEndereco),
            credentials: 'include',
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.erro || 'Erro desconhecido');
        }

        console.log(data.mensagem);
        return data;
    } catch (error) {
        console.error('Erro ao enviar endereço da agência:', error.message);
        throw error;
    }
}

export async function buscarEnderecoAgencia(id_agencia) {
    try {
        const response = await fetch(`http://localhost:5000/api/agencia/endereco?id=${id_agencia}`, {
            method: 'GET',
            credentials: 'include',
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.erro || 'Erro desconhecido');
        }

        return data;
    } catch (error) {
        console.error('Erro ao buscar endereço da agência:', error.message);
        throw error;
    }
}

export const getAgencias = async () => {
    try {
        const response = await fetch('http://localhost:5000/api/agencias');

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.erro || 'Erro ao buscar agências');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao buscar agências:', error.message);
        throw new Error(error.message || 'Erro desconhecido ao buscar agências');
    }
};


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

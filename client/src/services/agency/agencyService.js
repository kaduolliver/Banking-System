export const getAgencias = async () => {
    try {
        const response = await fetch(`http://localhost:5000/api/agencias`);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.erro || 'Erro ao buscar agências');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao buscar agências:', error.message);
        throw error;
    }
};

export async function cadastrarEnderecoAgencia(agenciaId, dadosEndereco) {
    try {
        const response = await fetch(`http://localhost:5000/api/agencias/${agenciaId}/endereco`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dadosEndereco),
            credentials: 'include',
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.erro || 'Erro desconhecido ao cadastrar endereço');
        }

        return data.endereco ?? data;
    } catch (error) {
        console.error('Erro ao cadastrar endereço da agência:', error.message);
        throw error;
    }
}

export async function atualizarEnderecoAgencia(agenciaId, dadosEndereco) {
    // console.log('agenciaId:', agenciaId);
    // console.log('dadosEndereco (enviados):', dadosEndereco);
    // console.log('URL da requisição:', `http://localhost:5000/api/agencias/${agenciaId}/endereco`);
    try {
        const response = await fetch(`http://localhost:5000/api/agencias/${agenciaId}/endereco`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dadosEndereco),
            credentials: 'include',
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.erro || 'Erro desconhecido ao atualizar endereço');
        }

        if (Array.isArray(data)) {
            return data[0];
        }

        return data.endereco ?? data;
    } catch (error) {
        console.error('Erro ao atualizar endereço da agência:', error.message);
        throw error;
    }
}

export async function buscarEnderecoAgencia(agenciaId) {
    try {
        const response = await fetch(`http://localhost:5000/api/agencias/${agenciaId}/endereco`, {
            method: 'GET',
            credentials: 'include',
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.erro || 'Erro desconhecido ao buscar endereço');
        }

        return data.endereco;
    } catch (error) {
        console.error('Erro ao buscar endereço da agência:', error.message);
        throw error;
    }
}

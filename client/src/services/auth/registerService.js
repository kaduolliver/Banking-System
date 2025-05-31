export async function registerUsuario(dados) {
   
    try {
        const res = await fetch('http://localhost:5000/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify(dados)
    });
    
        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.erro || 'Erro desconhecido no registro.');
        }

        return data;
    } catch (error) {
        console.error("Erro no registro:", error.message);
        throw error;
    }
}
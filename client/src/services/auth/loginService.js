export async function LoginUsuario(dados) {
   
    try {
        const res = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify(dados)
    });
    
        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.erro || 'Erro desconhecido no login.');
        }

        return data;
    } catch (error) {
        console.error("Erro no login:", error.message);
        throw error;
    }
}

export async function VerificaOTP(dados) {
    try {
        const res = await fetch('http://localhost:5000/api/validar-otp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados),
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.erro || 'Erro na verificação do OTP.');
        }

        return data; 
    } catch (error) {
        console.error('Erro na verificação do OTP:', error.message);
        throw error;
    }
}
export async function LoginUsuario(dados) {

    try {
        const res = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados),
            credentials: 'include',
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
            credentials: 'include',
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

export async function verificarSessao() {
    try {
        const res = await fetch('http://localhost:5000/api/sessao', {
            method: 'GET',
            credentials: 'include',
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.erro || 'Sessão não encontrada.');
        }

        return data;
    } catch (error) {
        console.error("Erro ao verificar sessão:", error.message);
        throw error;
    }
}

export async function logoutUsuario() {
  try {
    const res = await fetch('http://localhost:5000/api/logout', {
      method: 'POST',
      credentials: 'include',
    });

    if (!res.ok) {
      const data = await res.json();
      throw new Error(data.erro || 'Erro no logout.');
    }

    return await res.json();
  } catch (error) {
    console.error('Erro no logout:', error.message);
    throw error;
  }
}

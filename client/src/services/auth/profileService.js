export async function getMeuPerfil() {
  try {
    const res = await fetch('http://localhost:5000/api/me', {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.message || 'Erro ao buscar perfil');
    }

    const data = await res.json();
    return data;
  } catch (error) {
    throw new Error(error.message);
  }
}

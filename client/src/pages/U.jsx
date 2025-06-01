import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { verificarSessao } from '../services/auth/loginService';

export default function User() {
  const [carregando, setCarregando] = useState(true);
  const [alerta, setAlerta] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const checarSessao = async () => {
      try {
        const sessao = await verificarSessao();
        const tipo = sessao.tipo;
        if (tipo === 'cliente') navigate('/user/client');
        else if (tipo === 'funcionario') navigate('/user/employee');
        else throw new Error('Tipo de usuário desconhecido');
      } catch (error) {
        console.error('Sessão inválida ou expirada:', error);
        setAlerta('Você precisa iniciar sessão para acessar esta página.');
      } finally {
        setCarregando(false);
      }
    };

    checarSessao();
  }, [navigate]);

  if (carregando) return null;

  if (alerta) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-gray-100 text-center">
        <p className="mb-4 text-red-600 font-semibold">{alerta}</p>
        <a
          href="/login"
          className="px-6 py-3 bg-amber-600 text-white rounded hover:bg-amber-700 transition"
        >
          Ir para Login
        </a>
      </div>
    );
  }

  return null; // Não precisa renderizar nada ? redireciona automaticamente
}

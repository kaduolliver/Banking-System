import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/authContext';

export default function User() {
  const { usuario, carregando } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!carregando) {
      if (!usuario) {
        navigate('/login');
      } else if (usuario.tipo_usuario === 'cliente') {
        navigate('/user/client');
      } else if (usuario.tipo_usuario === 'funcionario') {
        navigate('/user/employee');
      } else {
        navigate('/login');
      }
    }
  }, [usuario, carregando, navigate]);

  // Enquanto estiver carregando, você pode exibir um loading, ou apenas o fundo preto
  if (carregando) {
    return (
      <div className="min-h-screen w-full bg-black flex items-center justify-center">
        {/* Opcional: loading spinner ou texto */}
        {/* <p className="text-white">Carregando...</p> */}
      </div>
    );
  }

  // Enquanto decide o redirecionamento, mantém o fundo para evitar o salto de layout
  return <div className="min-h-screen w-full bg-black" />;
}

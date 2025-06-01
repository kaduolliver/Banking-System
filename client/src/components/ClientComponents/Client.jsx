import { useEffect, useState } from 'react';
import ClientTabs from './ClientTabs';
import ClientNavbar from './ClientNavBar';
import { verificarSessao } from '../../services/auth/loginService';

export default function User() {
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    const checarSessao = async () => {
      try {
        await verificarSessao();
      } catch (error) {
        console.error('Sessão inválida ou expirada:', error);
        window.location.href = '/login';
      } finally {
        setCarregando(false);
      }
    };

    checarSessao();
  }, []);

  if (carregando) return null;

  return (
    <>
      <ClientNavbar />
      <div
        className="min-h-screen flex pt-40 pb-20 items-center justify-center bg-cover p-6"
        style={{ backgroundImage: "url('/images/bitcoin-bg-user.png')" }}
      >
        <ClientTabs />
      </div>
    </>
  );
}

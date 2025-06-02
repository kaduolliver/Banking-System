import { useAuth } from '../../context/authContext';
import ClientTabs from './ClientTabs';
import ClientNavbar from './ClientNavBar';
import ScreenOverlay from '../EffectsComponents/ScreenOverlay';
import { Navigate } from 'react-router-dom';

export default function Client() {
  const { carregando, usuario } = useAuth();

  if (carregando) return null;

  if (usuario?.tipo_usuario !== 'cliente') return <Navigate to="/login" />;

  return (
    <>
      <ScreenOverlay />
      <ClientNavbar />
      <div
        className="min-h-screen flex pt-40 pb-20 bg-black items-center justify-center bg-cover p-6"
        style={{ backgroundImage: "url('/images/bitcoin-bg-user.png')" }}
      >
        <ClientTabs />
      </div>
    </>
  );
}
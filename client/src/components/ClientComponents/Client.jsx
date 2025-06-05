import { useAuth } from '../../context/authContext';
import ClientTabs from './ClientTabs';
import ClientNavbar from './ClientNavBar';
import ScreenOverlay from '../EffectsComponents/ScreenOverlay';
import SplashScreen from '../EffectsComponents/SplashScreen';

export default function Client() {

  const { carregando } = useAuth();

  if (carregando) return <SplashScreen />;

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
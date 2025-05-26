import { useEffect, useState } from 'react';
import UserTabs from '../components/UserComponents/UserTabs';
import Client from '../components/UserComponents/Client';
import Employee from '../components/UserComponents/Employee';
import { UserIcon, SettingsIcon } from 'lucide-react'; 
import Navbar from '../components/navbar';

export default function User() {
  const [activeTab, setActiveTab] = useState('perfil');
  const [userType, setUserType] = useState(null); // 'client' ou 'employee'

  useEffect(() => {
    // Simulação do tipo de usuário (ex: vindo do backend ou contexto)
    const fakeUserType = 'client'; // trocar para 'employee' para testar
    setUserType(fakeUserType);
  }, []);

  if (!userType) return null;

  const isClient = userType === 'client';
  const contentComponent = isClient ? <Client /> : <Employee />;

  const tabs = [
    {
      value: 'perfil',
      label: 'Meu Perfil',
      icon: UserIcon,
      content: contentComponent,
    },
    {
      value: 'config',
      label: 'Configurações',
      icon: SettingsIcon,
      content: (
        <div>
          <h2 className="text-xl font-bold mb-2">Configurações</h2>
          <p className="text-gray-300">Aqui você poderá configurar sua conta.</p>
        </div>
      ),
    },
  ];

  return (
    <>
    <Navbar />
    <div className="min-h-screen flex items-center justify-center bg-cover p-6" style={{ backgroundImage: "url('/images/bitcoin-bg-user.png')" }}>
      <UserTabs tabs={tabs} activeTab={activeTab} setActiveTab={setActiveTab} />
    </div>
    </>
  );
}

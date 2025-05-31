import { useState } from 'react';
import { UserIcon, SettingsIcon } from 'lucide-react';
import UserTab from '../UserComponents/UserTab';

export default function EmployeeTabs() {
  const [activeTab, setActiveTab] = useState('perfil');

  const tabs = [
    {
      value: 'perfil',
      label: 'Meu Perfil',
      icon: UserIcon,
    },
    {
      value: 'config',
      label: 'Configura��es',
      icon: SettingsIcon,
      content: (
        <div>
          <h2 className="text-xl font-bold mb-2">Configura��es</h2>
          <p className="text-gray-300">Configura��es da conta do cliente.</p>
        </div>
      ),
    },
  ];

  return <UserTab tabs={tabs} activeTab={activeTab} setActiveTab={setActiveTab} />;
}

import { useState } from 'react';
import { ShieldUser, SettingsIcon } from 'lucide-react';
import UserTab from '../UserComponents/UserTab';
import AdmPersonalData from '../EmployeeComponents/EmployeeTabs/AdmEmployee/AdmPersonalData';

export default function EmployeeTabs() {
  const [activeTab, setActiveTab] = useState('dados');

  const tabs = [
    {
      value: 'dados',
      label: 'Dados Pessoais',
      icon: ShieldUser,
      content: < AdmPersonalData />
    },
    {
      value: 'config',
      label: 'Configurações',
      icon: SettingsIcon,
      content: (
        <div>
          <h2 className="text-xl font-bold mb-2">Configurações</h2>
          <p className="text-gray-300">Configurações da conta do cliente.</p>
        </div>
      ),
    },
  ];

  return <UserTab tabs={tabs} activeTab={activeTab} setActiveTab={setActiveTab} />;
}

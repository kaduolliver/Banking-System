import { useState } from 'react';
import { ShieldUser, SettingsIcon, HandCoins, SlidersHorizontal, ClipboardList, Building } from 'lucide-react';
import UserTab from '../UserComponents/UserTab';
import AdmPersonalData from '../EmployeeComponents/EmployeeTabs/AdmEmployee/AdmPersonalData';
import FinancialRequests from '../EmployeeComponents/EmployeeTabs/AdmEmployee/FinancialRequests'
//import ManagerConfig from '../EmployeeComponents/EmployeeTabs/AdmEmployee/ManagerConfig';
//import ReportsConfig from '../EmployeeComponents/EmployeeTabs/AdmEmployee/ReportsConfig';
import AgencyConfig from '../EmployeeComponents/EmployeeTabs/AdmEmployee/AgencyConfig';

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
      value: 'manager',
      label: 'Gerenciamento',
      icon: SlidersHorizontal,
      //content: < ManagerConfig />
    },
    {
      value: 'agency',
      label: 'Agência',
      icon: Building,
      content: < AgencyConfig />
    },
    {
      value: 'requests',
      label: 'Solicitações',
      icon: HandCoins,
      content: < FinancialRequests />
    },
    {
      value: 'reports',
      label: 'Relatórios',
      icon: ClipboardList,
      //content: < ReportsConfig />
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

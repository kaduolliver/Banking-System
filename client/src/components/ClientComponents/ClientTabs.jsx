import { useState } from 'react';
import { UserIcon, SettingsIcon, CircleDollarSign, Wallet, Bitcoin, CreditCard, HandCoins } from 'lucide-react';
import UserTab from '../UserComponents/UserTab';
import AccountPanel from './ClientTabs/ClientAccountPanel';
import PersonalData from './ClientTabs/ClientPersonalData';
//import FinancialServices from './ClientTabs/ClientFinancialServices';
import ClientRequests from './ClientTabs/ClientRequests';

export default function ClientTabs() {
    const [activeTab, setActiveTab] = useState('conta');

    const tabs = [
        {
            value: 'conta',
            label: 'Minha Conta',
            icon: Wallet,
            content: <AccountPanel />,
        },
        {
            value: 'dados',
            label: 'Dados Pessoais',
            icon: UserIcon,
            content: <PersonalData />,
        },
        {
            value: 'accountRequest',
            label: 'Solicitações',
            icon: HandCoins,
            content: <ClientRequests />
        },  
        {
            value: 'servicos',
            label: 'Financeiro',
            icon: CircleDollarSign,
            //content: <FinancialServices />,
        },
        // {
        //     value: 'cripto',
        //     label: 'Cripto',
        //     icon: Bitcoin,
        //     //content: <CriptoServices />,
        // },
        {
            value: 'cartao',
            label: 'Cartão',
            icon: CreditCard,
            //content: <CreditCardServices />,
        },
        {
            value: 'config',
            label: 'Configurações',
            icon: SettingsIcon,
            //content: <ConfigServices />,
        },
    ];
    
    return <UserTab tabs={tabs} activeTab={activeTab} setActiveTab={setActiveTab} />;
}

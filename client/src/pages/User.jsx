import { useState } from 'react'
import ScreenOverlay from "../components/ScreenOverlay";
import UserTabs from '../components/UserTabs';
import {
    LayoutDashboard,
    Wallet,
    Settings,
    Bell,
    Shield,
    LifeBuoy,
} from 'lucide-react'

const tabs = [
    { value: 'tab1', label: 'Dashboard', icon: LayoutDashboard, content: 'Painel geral' },
    { value: 'tab2', label: 'Carteira', icon: Wallet, content: 'Seus ativos digitais' },
    { value: 'tab3', label: 'Configurações', icon: Settings, content: 'Preferências do usuário' },
    { value: 'tab4', label: 'Notificações', icon: Bell, content: 'Alertas e mensagens' },
    { value: 'tab5', label: 'Segurança', icon: Shield, content: 'Verificação em duas etapas' },
    { value: 'tab6', label: 'Suporte', icon: LifeBuoy, content: 'Central de ajuda' },
]


export default function User() {
    const [activeTab, setActiveTab] = useState('tab1')

    return (
        <>
            <ScreenOverlay />
            <div className="pt-20 min-h-screen bg-cover bg-center bg-slate-950">
                <div className="p-8">
                    <h1 className="text-white text-2xl mb-4">Área do Usuário</h1>
                    <UserTabs tabs={tabs} activeTab={activeTab} setActiveTab={setActiveTab} />
                </div>
            </div>
        </>
    )
}

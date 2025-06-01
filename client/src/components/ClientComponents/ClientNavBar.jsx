import { Link, useNavigate } from "react-router-dom";
import { Globe, Banknote, User, Bell, Landmark } from "lucide-react";
import { logoutUsuario } from '../../services/auth/loginService'; // importe a função logout que criamos

const ClientNavbar = () => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logoutUsuario();
      localStorage.removeItem('tipo');
      navigate('/login');
    } catch (error) {
      alert('Erro ao fazer logout. Tente novamente.');
    }
  };

  return (
    <header className="bg-black text-white shadow-ms w-full fixed top-0 left-0 z-[50]">
      <div className="w-full mx-auto px-6 py-6 flex items-center justify-between">
        {/* Logo à esquerda */}
        <Link to="/" className="text-5xl relative left-10" style={{ fontFamily: 'Bodoni FLF' }}> I&L </Link>

        {/* Navegação central */}
        <nav className="space-x-8 hidden md:flex gap-20" style={{ fontFamily: 'Aileron, sans-serif' }}>
          <Link to="/user" className="group relative flex items-center gap-2 top-1 text-white font-bold transition hover:text-amber-400">
            <User className="relative bottom-1" />
            <span>Meu Perfil</span>
            <span className="absolute left-0 -bottom-1 w-0 h-0.5 bg-gradient-to-r from-yellow-400 to-amber-600 transition-all duration-300 group-hover:w-full"></span>
          </Link>
          <Link to="/market" className="group flex relative font-bold gap-2 text-white transition hover:text-amber-400" style={{ fontFamily: 'Aileron, sans-serif' }}>
            <Landmark />
            <span className="relative top-1">Mercado</span>
            <span className="absolute left-0 -bottom-1 w-0 h-0.5 bg-gradient-to-r from-yellow-400 to-amber-600 transition-all duration-300 group-hover:w-full"></span>
          </Link>
          <Link
            to="/login"
            className="hover:text-amber-400 flex font-bold items-center gap-2 transition relative top-1"
          >
            <Banknote />
            Saldo
          </Link>
        </nav>

        {/* Lado direito */}
        <div className="relative right-10 flex items-center gap-10" style={{ fontFamily: 'Aileron, sans-serif' }}>
          <button
            onClick={handleLogout}
            className="px-6 py-2 relative left-4 bg-gradient-to-r from-amber-600 to-orange-700 hover:from-orange-700 hover:to-amber-600 text-white font-bold rounded-lg transition"
          >
            Encerrar Sessão
          </button>
          <button className="hover:text-amber-400 transition relative left-5" title="Notificações">
            <Bell className="size-7" />
          </button>
          <button className="hover:text-amber-400 transition relative top-2 left-8" title="Mudar idioma">
            <Globe />
            <p className="text-sm relative right-2">PT-BR</p>
          </button>
        </div>
      </div>
    </header>
  );
};

export default ClientNavbar;

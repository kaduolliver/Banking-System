import './App.css';
import { Routes, Route, useLocation } from 'react-router-dom';
import Home from './pages/Home';
import Market from './pages/Market';
import Login from './pages/Login';
import About from './pages/About';
import User from './pages/User';
import CreditCard from './pages/CreditCard';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import { AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';
import SplashScreen from './components/EffectsComponents/SplashScreen';
import Client from './components/ClientComponents/Client'
import Employee from './components/EmployeeComponents/Employee';
import ProtectedRoute from './components/ProtectedRoute';
import ClientNavbar from './components/ClientComponents/ClientNavBar';
import EmpNavBar from './components/EmployeeComponents/EmpNavBar';
import { verificarSessao } from './services/auth/loginService';

// Importa o ScrollToTop
import ScrollToTop from './components/EffectsComponents/ScrollToTop';

export default function App() {
  const [showSplash, setShowSplash] = useState(true);
  const location = useLocation();

  const [tipoUsuario, setTipoUsuario] = useState(null);

  useEffect(() => {
    const obterSessao = async () => {
      try {
        const sessao = await verificarSessao();
        setTipoUsuario(sessao.tipo_usuario); // 'cliente' ou 'funcionario'
      } catch {
        setTipoUsuario(null);
      }
    };
    obterSessao();
  }, []);

  const ocultarFooter = [''];

  return (
    <>
      <AnimatePresence>
        {showSplash && <SplashScreen onComplete={() => setShowSplash(false)} />}
      </AnimatePresence>

      {!showSplash && (
        // Main Container
        <div className="main-container">
          {/* Header */}
          <header className="header-content">
            {/* <Navbar /> */}
            {tipoUsuario === 'cliente' ? (
              <ClientNavbar />
            ) : tipoUsuario === 'funcionario' ? (
              <EmpNavBar />
            ) : (
              <Navbar />
            )}

          </header>

          {/* Adiciona ScrollToTop aqui */}
          <ScrollToTop />

          {/* Content */}
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/market" element={<Market />} />
              <Route path="/login" element={<Login />} />
              <Route path="/about" element={<About />} />
              <Route path="/user" element={<User />} />
              <Route path="/user/client" element={<ProtectedRoute><Client /></ProtectedRoute>} />
              <Route path="/user/employee" element={<ProtectedRoute><Employee /></ProtectedRoute>} />
              <Route path="/creditcard" element={<CreditCard />} />
            </Routes>
          </main>

          {/* Footer */}
          {!ocultarFooter.includes(location.pathname) && (
            <footer className="footer-content">
              <Footer />
            </footer>
          )}
        </div>
      )}
    </>
  );
}

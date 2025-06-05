import { createContext, useContext, useEffect, useState } from 'react';
import { verificarSessao, logoutUsuario } from '../services/auth/loginService';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    const carregarSessao = async () => {
      try {
        const sessao = await verificarSessao();
        if (sessao.autenticado) {
          setUsuario(sessao);
        } else {
          setUsuario(null);
        }
      } catch {
        setUsuario(null);
      } finally {
        setCarregando(false);
      }
    };
    carregarSessao();
  }, []);

  const logout = async () => {
    try {
      await logoutUsuario();      
    } catch (error) {
      console.error('Erro no logout:', error);
    }
    localStorage.removeItem('tipo'); 
    setUsuario(null);               
  };

  return (
    <AuthContext.Provider value={{ usuario, setUsuario, carregando, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);

import { createContext, useContext, useEffect, useState } from 'react';
import { verificarSessao } from '../services/auth/loginService';

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

  return (
    <AuthContext.Provider value={{ usuario, setUsuario, carregando }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);

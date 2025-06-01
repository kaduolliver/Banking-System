// components/ProtectedRoute.jsx
import { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { verificarSessao } from '../services/auth/loginService';

export default function ProtectedRoute({ children }) {
  const [autenticado, setAutenticado] = useState(null);

  useEffect(() => {
    const checar = async () => {
      try {
        await verificarSessao();
        setAutenticado(true);
      } catch {
        setAutenticado(false);
      }
    };
    checar();
  }, []);

  if (autenticado === null) return null; // ou loading

  return autenticado ? children : <Navigate to="/user" replace />;
}

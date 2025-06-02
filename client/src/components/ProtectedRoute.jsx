// components/ProtectedRoute.jsx
import { useAuth } from '../context/authContext';
import { Navigate } from 'react-router-dom';

export default function ProtectedRoute({ children, tipoPermitido = null }) {
  const { usuario, carregando } = useAuth();

  if (carregando) return null;

  if (!usuario) {
    return <Navigate to="/login" replace />;
  }

  if (tipoPermitido && usuario.tipo_usuario !== tipoPermitido) {
    return <Navigate to="/user" replace />;
  }

  return children;
}

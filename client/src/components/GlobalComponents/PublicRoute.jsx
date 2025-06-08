import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/authContext';

export default function PublicRoute({ children }) {
  const { usuario } = useAuth();
  const splashAtivo = localStorage.getItem('mostrandoSplash') === 'true';

  if (usuario && !splashAtivo) {
    return <Navigate to="/user" replace />;
  }

  return children;
}

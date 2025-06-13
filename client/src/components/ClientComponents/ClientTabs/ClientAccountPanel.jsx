import { useState, useEffect } from 'react';
import ClientAddressForm from './AccountPanelComponents/ClientAddress';
import AccountRequest from './AccountPanelComponents/ClientAccountRequest';
import ClientAccountInfo from './AccountPanelComponents/ClientAccountInfo';
import { useAuth } from '../../../context/authContext';
import { verificarConta } from '../../../services/cliente/contaService';
import { verificarSessao } from '../../../services/auth/loginService';

export default function ClientAccountPanel() {
  const { usuario, carregando, setUsuario } = useAuth();

  const [enderecoSalvo, setEnderecoSalvo] = useState(false);
  const [temConta, setTemConta] = useState(null);
  const [tiposConta, setTiposConta] = useState([]);

  useEffect(() => {
    const fetchConta = async () => {
      if (!carregando && usuario?.id_usuario) {
        try {
          const resposta = await verificarConta(usuario.id_usuario);
          setTemConta(resposta.temConta);
          setTiposConta(resposta.tiposConta || []);
        } catch {
          setTemConta(false);
          setTiposConta([]);
        }
      }
    };
    fetchConta();
  }, [carregando, usuario]);

  const handleSolicitacaoConcluida = async () => {
    try {
      const dadosAtualizados = await verificarSessao();
      setUsuario(dadosAtualizados.usuario);

      const resposta = await verificarConta(dadosAtualizados.id_usuario);
      setTemConta(resposta.temConta);
      setTiposConta(resposta.tiposConta || []);
    } catch (error) {
      console.error('Erro ao atualizar usuário após solicitação:', error);
    }
  };

  if (carregando || temConta === null) {
    return <p className="text-center text-gray-500">Carregando informações...</p>;
  }

  return (
    <div>
      {!enderecoSalvo && (
        <ClientAddressForm onEnderecoSalvo={() => setEnderecoSalvo(true)} />
      )}

      {enderecoSalvo && temConta && (
        <ClientAccountInfo tiposConta={tiposConta} />
      )}

      {enderecoSalvo && !temConta && (
        <AccountRequest onSolicitacaoConcluida={handleSolicitacaoConcluida} />
      )}
    </div>
  );
}
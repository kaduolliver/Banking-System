import { useEffect, useState } from 'react';
import { getSolicitacoesPendentes, aprovarSolicitacao, rejeitarSolicitacao } from '../../../../services/employee/requestsService';
import { useAuth } from '../../../../context/authContext'; 

export default function FinancialRequests() {
  const { usuario, carregando: carregandoAuth } = useAuth();
  const [solicitacoes, setSolicitacoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(null);
  const [erro, setErro] = useState(null);
  
  useEffect(() => {
    if (!carregandoAuth && usuario?.cargo === 'Admin' || usuario?.cargo === 'Gerente') {
      fetchSolicitacoes();
    }
  }, [carregandoAuth, usuario]);

  const fetchSolicitacoes = async () => {
    setLoading(true);
    try {
      const data = await getSolicitacoesPendentes();
      setSolicitacoes(data);
    } catch (error) {
      setErro('Erro ao carregar solicitações.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleAprovar = async (id) => {
    setProcessing(id);
    try {
      await aprovarSolicitacao(id);
      setSolicitacoes(prev => prev.filter(s => s.id_solicitacao !== id));
    } catch (error) {
      console.error(error);
      setErro('Erro ao aprovar solicitação.');
    } finally {
      setProcessing(null);
    }
  };

  const handleRejeitar = async (id) => {
    setProcessing(id);
    try {
      await rejeitarSolicitacao(id);
      setSolicitacoes(prev => prev.filter(s => s.id_solicitacao !== id));
    } catch (error) {
      console.error(error);
      setErro('Erro ao rejeitar solicitação.');
    } finally {
      setProcessing(null);
    }
  };

  if (carregandoAuth) return <p className="text-gray-300">Verificando autenticação...</p>;

  if (!usuario || (usuario.cargo !== 'Admin' && usuario.cargo !== 'Gerente')) {
    return <p className="text-red-400">Acesso negado. Permissão insuficiente.</p>;
  }

  if (loading) return <p className="text-gray-300">Carregando solicitações...</p>;

  if (solicitacoes.length === 0) {
    return <p className="text-gray-400">Nenhuma solicitação pendente.</p>;
  }

  return (
    <div className="space-y-4">
      {erro && <div className="bg-red-500 text-white p-2 rounded">{erro}</div>}
      {solicitacoes.map((s) => (
        <div key={s.id_solicitacao} className="bg-gray-800 text-white rounded-2xl shadow p-4">
          <p><strong>Cliente:</strong> {s.nome_cliente}</p>
          <p><strong>Tipo de Conta:</strong> {s.tipo_conta}</p>
          <p><strong>Valor Inicial:</strong> R$ {parseFloat(s.valor_inicial || 0).toFixed(2)}</p>
          <p><strong>Data:</strong> {new Date(s.data_solicitacao).toLocaleString()}</p>
          <div className="mt-4 flex gap-2">
            <button
              onClick={() => handleAprovar(s.id_solicitacao)}
              className="px-4 py-2 rounded-2xl bg-green-600 hover:bg-green-700 text-white font-semibold disabled:opacity-50"
              disabled={processing === s.id_solicitacao}
            >
              {processing === s.id_solicitacao ? 'Aprovando...' : 'Aprovar'}
            </button>
            <button
              onClick={() => handleRejeitar(s.id_solicitacao)}
              className="px-4 py-2 rounded-2xl bg-red-600 hover:bg-red-700 text-white font-semibold disabled:opacity-50"
              disabled={processing === s.id_solicitacao}
            >
              {processing === s.id_solicitacao ? 'Rejeitando...' : 'Rejeitar'}
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

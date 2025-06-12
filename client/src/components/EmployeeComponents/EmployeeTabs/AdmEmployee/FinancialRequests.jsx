import { useEffect, useState } from 'react';
import { getSolicitacoesPendentes, aprovarSolicitacao, rejeitarSolicitacao } from '../../../../services/employee/requestsService';
import { useAuth } from '../../../../context/authContext';

export default function FinancialRequests() {
  const { usuario, carregando: carregandoAuth } = useAuth();
  const [solicitacoes, setSolicitacoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(null);
  const [erro, setErro] = useState(null);
  const [removendo, setRemovendo] = useState([]);

  useEffect(() => {
    if (!carregandoAuth && usuario?.cargo === 'Admin' || usuario?.cargo === 'Gerente' || usuario?.cargo === 'Estagiário') {
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

  const removerComAnimacao = (id) => {
    setRemovendo((prev) => [...prev, id]);
    setTimeout(() => {
      setSolicitacoes((prev) => prev.filter((s) => s.id_solicitacao !== id));
      setRemovendo((prev) => prev.filter((rid) => rid !== id));
    }, 500);
  };

  const handleAprovar = async (id) => {
    setProcessing(id);
    try {
      await aprovarSolicitacao(id);
      removerComAnimacao(id);
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
      removerComAnimacao(id);
    } catch (error) {
      console.error(error);
      setErro('Erro ao rejeitar solicitação.');
    } finally {
      setProcessing(null);
    }
  };

  const isManager = usuario?.tipo_usuario === 'funcionario' && (usuario?.cargo === 'Admin' || usuario?.cargo === 'Gerente');

  if (carregandoAuth) return <p className="text-xl font-semibold mt-6 text-center text-gray-400">Verificando autenticação...</p>;

  if (!usuario || (usuario.cargo !== 'Admin' && usuario.cargo !== 'Gerente' && usuario.cargo !== 'Estagiário')) {
    return <p className="text-xl font-semibold mt-6 text-center text-red-400">Acesso negado. Permissão insuficiente.</p>;
  }

  if (loading) return <p className="text-xl font-semibold mt-6 text-center text-gray-400">Carregando solicitações...</p>;

  if (solicitacoes.length === 0) {
    return <p className="text-xl font-semibold mt-6 text-center text-gray-400">Nenhuma solicitação pendente.</p>;
  }

  return (
    <div className="space-y-2">
      {erro && (
        <div className="bg-red-500 text-white px-3 py-2 rounded-lg shadow-sm">
          {erro}
        </div>
      )}

      {solicitacoes.map((s) => {
        const estaRemovendo = removendo.includes(s.id_solicitacao);

        return (
          <div
            key={s.id_solicitacao}
            className={`bg-gradient-to-br from-gray-900 to-gray-800 text-white rounded-2xl shadow-lg p-4 transform transition-all duration-300 ${estaRemovendo ? 'translate-x-full opacity-0' : ''
              }`}
          >
            <div className="space-y-1 text-sm">
              <p>
                <span className="font-medium text-gray-400">Cliente:</span>{' '}
                <span className="font-semibold">{s.nome_cliente}</span>
              </p>
              <p>
                <span className="font-medium text-gray-400">Tipo de Conta:</span>{' '}
                <span className="font-semibold">{s.tipo_conta}</span>
              </p>
              <p>
                <span className="font-medium text-gray-400">Valor Inicial:</span>{' '}
                <span className="font-semibold">R$ {parseFloat(s.valor_inicial || 0).toFixed(2)}</span>
              </p>
              <p>
                <span className="font-medium text-gray-400">Data:</span>{' '}
                <span className="font-semibold">{new Date(s.data_solicitacao).toLocaleString()}</span>
              </p>
            </div>

            {isManager && (
              <div className="mt-4 flex gap-3">
                <button
                  onClick={() => handleAprovar(s.id_solicitacao)}
                  className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={processing === s.id_solicitacao}
                >
                  {processing === s.id_solicitacao ? 'Aprovando...' : 'Aprovar'}
                </button>
                <button
                  onClick={() => handleRejeitar(s.id_solicitacao)}
                  className="px-4 py-2 rounded-lg bg-rose-600 hover:bg-rose-700 text-white font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={processing === s.id_solicitacao}
                >
                  {processing === s.id_solicitacao ? 'Rejeitando...' : 'Rejeitar'}
                </button>
              </div>
            )}

          </div>
        );
      })}
    </div>
  );
}

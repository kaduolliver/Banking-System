import { motion, AnimatePresence } from 'framer-motion';
import { useEffect, useState, useCallback } from 'react';

// import {
//   getSolicitacoesEmprestimosPendentes,
//   aprovarSolicitacao,
//   rejeitarSolicitacao,
// } from '../../../../services/employee/requestsService';
import { useAuth } from '../../../../../context/authContext';

export default function FinancialRequests() {
  const { usuario, carregando: carregandoAuth } = useAuth();
  const [solicitacoes, setSolicitacoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(null);
  const [erro, setErro] = useState(null);

  const isManager =
    usuario?.tipo_usuario === 'funcionario' &&
    ['Admin', 'Gerente'].includes(usuario?.cargo);

  const fetchSolicitacoes = useCallback(async () => {
    try {
      setLoading(true);
      const data = await getSolicitacoesEmprestimosPendentes();
      setSolicitacoes(data);
    } catch (err) {
      console.error(err);
      setErro('Erro ao carregar solicitações.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!carregandoAuth && usuario) fetchSolicitacoes();
  }, [carregandoAuth, usuario, fetchSolicitacoes]);

  const processSolicitacao = async (id, actionFn) => {
    try {
      setProcessing(id);
      await actionFn(id);
      setSolicitacoes((prev) => prev.filter((s) => s.id_solicitacao !== id));
    } catch (err) {
      console.error(err);
      setErro('Ocorreu um erro. Tente novamente.');
    } finally {
      setProcessing(null);
    }
  };

  const LoadingOrEmpty = ({ children, className = '' }) => (
    <div
      className={`max-w-3xl mx-auto mt-10 p-6 bg-black rounded-2xl shadow-lg text-center text-gray-400 ${className}`}
    >
      {children}
    </div>
  );

  if (carregandoAuth)
    return <LoadingOrEmpty>Verificando autenticação…</LoadingOrEmpty>;

  if (!usuario || (!isManager && usuario.cargo !== 'Estagiário'))
    return (
      <LoadingOrEmpty className="text-red-400">
        Acesso negado. Permissão insuficiente.
      </LoadingOrEmpty>
    );

  return (
    <div className="max-w-5xl mx-auto mt-10 p-4 bg-black rounded-2xl shadow-lg text-white">
      <TabBody
        solicitacoes={solicitacoes}
        loading={loading}
        erro={erro}
        isManager={isManager}
        processing={processing}
        processSolicitacao={processSolicitacao}
        isLoan
      />
    </div>
  );
}

function TabBody({
  solicitacoes,
  loading,
  erro,
  isManager,
  processing,
  processSolicitacao,
  isLoan = false,
}) {
  if (loading) {
    return (
      <p className="text-center text-gray-400">Carregando solicitações…</p>
    );
  }

  if (solicitacoes.length === 0) {
    return (
      <p className="text-center text-gray-400">Nenhuma solicitação pendente.</p>
    );
  }

  return (
    <>
      {erro && (
        <div className="mb-4 bg-rose-600/20 border border-rose-600 text-rose-300 px-4 py-2 rounded-lg">
          {erro}
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <AnimatePresence initial={false}>
          {solicitacoes.map((s) => (
            <motion.div
              key={s.id_solicitacao}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ duration: 0.2 }}
              className="rounded-2xl bg-gradient-to-br from-gray-900 to-gray-800 p-4 shadow-md"
            >
              <div className="space-y-1 text-xs sm:text-sm">
                <p>
                  <span className="font-medium text-gray-400">Cliente:</span>{' '}
                  <span className="font-semibold">{s.nome_cliente}</span>
                </p>
                <p>
                  <span className="font-medium text-gray-400">Valor:</span>{' '}
                  R$ {Number(s.valor_solicitado || 0).toFixed(2)}
                </p>
                <p>
                  <span className="font-medium text-gray-400">Parcelas:</span>{' '}
                  {s.qtd_parcelas}
                </p>
                <p>
                  <span className="font-medium text-gray-400">Data:</span>{' '}
                  {new Date(s.data_solicitacao).toLocaleDateString()}{' '}
                  {new Date(s.data_solicitacao).toLocaleTimeString([], {
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </p>
              </div>

              {isManager && (
                <div className="mt-3 flex gap-2">
                  <button
                    onClick={() =>
                      processSolicitacao(s.id_solicitacao, aprovarSolicitacao)
                    }
                    className="flex-1 px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-xs sm:text-sm font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    disabled={processing === s.id_solicitacao}
                  >
                    {processing === s.id_solicitacao ? 'Aprovando…' : 'Aprovar'}
                  </button>
                  <button
                    onClick={() =>
                      processSolicitacao(s.id_solicitacao, rejeitarSolicitacao)
                    }
                    className="flex-1 px-3 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-700 text-xs sm:text-sm font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    disabled={processing === s.id_solicitacao}
                  >
                    {processing === s.id_solicitacao ? 'Rejeitando…' : 'Rejeitar'}
                  </button>
                </div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </>
  );
}

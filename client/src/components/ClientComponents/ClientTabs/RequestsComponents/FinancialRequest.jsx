import { useState, useEffect } from "react";
import { useAuth } from '../../../../context/authContext';
import { solicitarEmprestimo } from '../../../../services/cliente/contaService';
import { formatarMoeda, desformatarMoeda } from "../../../../utils/formatters";

export default function FinancialRequest() {
  const { usuario } = useAuth();
  const contas = usuario?.contas || [];
  const emprestimos = usuario?.emprestimos || [];

  // Estado do formulário
  const [valor, setValor] = useState("");
  const [prazo, setPrazo] = useState(12);
  const [finalidade, setFinalidade] = useState("");
  const [contaSelecionada, setContaSelecionada] = useState(contas.length > 0 ? contas[0].id_conta : "");
  const [enviouSolicitacao, setEnviouSolicitacao] = useState(false);
  const [mensagem, setMensagem] = useState("");
  const [erro, setErro] = useState("");

  useEffect(() => {
    if (contas.length > 0 && !contaSelecionada) {
      setContaSelecionada(contas[0].id_conta);
    }
  }, [contas, contaSelecionada]);

  // Lógica para bloquear o formulário baseado no status do empréstimo mais recente
  const ultimoEmprestimo = emprestimos.length > 0
    ? emprestimos[emprestimos.length - 1] // assumindo que o último é o mais recente
    : null;

  // Função para validar se está bloqueado e o motivo
  const getStatusBloqueio = () => {
    if (enviouSolicitacao) return 'pendente';

    if (!ultimoEmprestimo) return null;
    const status = ultimoEmprestimo.status?.toUpperCase();

    if (status === 'PENDENTE') {
      return 'pendente';
    }
    if (status === 'REJEITADO') {
      return 'rejeitado';
    }
    if (status === 'APROVADO') {
      return 'aprovada';
    }
    return null;
  };

  const statusBloqueio = getStatusBloqueio();

  const validarDados = () => {
    const valorNum = desformatarMoeda(valor);
    if (isNaN(valorNum) || valorNum < 1000 || valorNum > 100000) {
      setErro("Valor deve estar entre R$1.000 e R$100.000.");
      return false;
    }
    if (prazo < 6 || prazo > 60) {
      setErro("Prazo deve estar entre 6 e 60 meses.");
      return false;
    }
    if (!finalidade.trim()) {
      setErro("Finalidade é obrigatória.");
      return false;
    }
    if (!contaSelecionada) {
      setErro("Selecione uma conta para depósito.");
      return false;
    }
    setErro("");
    return true;
  };

  const handleChangeValor = (e) => {
    const apenasDigitos = e.target.value.replace(/\D/g, "");
    setValor(formatarMoeda(apenasDigitos));
  };

  const handleSubmit = async () => {
    if (!validarDados()) return;
    const valorNumerico = desformatarMoeda(valor);
    setMensagem("");
    setErro("");

    try {
      await solicitarEmprestimo({
        id_usuario: usuario.id_usuario,
        valor_solicitado: valorNumerico,
        prazo_meses: prazo,
        finalidade: finalidade.trim(),
        id_conta: parseInt(contaSelecionada),
      });

      setMensagem("Solicitação de empréstimo enviada com sucesso!");
      setValor("");
      setPrazo(12);
      setFinalidade("");
      setEnviouSolicitacao(true);
    } catch (e) {
      setErro(e.message || "Erro ao solicitar empréstimo.");
    }
  };

  // Renderizações especiais para status bloqueados:
  if (statusBloqueio === 'pendente') {
    return (
      <div className="max-w-xl mx-auto mt-10 p-6 bg-black shadow-lg rounded-2xl text-center">
        <h2 className="text-2xl font-semibold mb-4 text-gray-200">
          Solicitação Pendente
        </h2>
        <p className="text-blue-400">
          Você já possui um empréstimo com status <strong>PENDENTE</strong>.<br />
          Aguarde a análise da sua solicitação.
        </p>
      </div>
    );
  }

  if (statusBloqueio === 'rejeitado') {
    return (
      <div className="max-w-xl mx-auto mt-10 p-6 bg-black shadow-lg rounded-2xl text-center">
        <h2 className="text-2xl font-semibold mb-4 text-gray-200">
          Empréstimo Rejeitado
        </h2>
        <p className="text-red-400">
          Sua última solicitação foi <strong>REJEITADA</strong>.<br />
          Você está bloqueado para novas solicitações por um período determinado.
        </p>
      </div>
    );
  }

  if (statusBloqueio === 'aprovada') {
    return (
      <div className="max-w-xl mx-auto mt-10 p-6 bg-black shadow-lg rounded-2xl text-center">
        <h2 className="text-2xl font-semibold mb-4 text-gray-200">
          Solicitação Aprovada
        </h2>
        <p className="text-green-400">
          Você já possui um empréstimo <strong>APROVADO</strong>.<br />
          Novas solicitações estarão bloqueadas por um período determinado.
        </p>
      </div>
    );
  }

  return (
    <div className="p-6 bg-gray-900 rounded-xl shadow-md font-sans max-w-xl mx-auto">
      <h3 className="text-xl font-semibold mb-6 text-orange-400 text-center">
        Solicitar Empréstimo
      </h3>

      {!usuario || contas.filter(c => c.tipo === 'corrente').length === 0 ? (
        <p className="text-red-400 text-center">
          Nenhuma conta corrente disponível para solicitação de empréstimo.
          Por favor, abra uma conta <strong>corrente</strong> primeiro.
        </p>
      ) : (
        <>
          <div className="mb-4">
            <label className="block mb-1 text-sm text-gray-300" htmlFor="conta-select">Conta para Depósito:</label>
            <select
              id="conta-select"
              value={contaSelecionada}
              onChange={(e) => setContaSelecionada(e.target.value)}
              className="w-full px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-600 focus:outline-none focus:border-orange-500"
            >
              {contas
                .filter(conta => conta.tipo === 'corrente')
                .map((conta) => (
                  <option key={conta.id_conta} value={conta.id_conta}>
                    {conta.numero_conta} ({conta.tipo}) -  Agência: {conta.agencia}
                  </option>
                ))}
            </select>
          </div>

          <div className="mb-4">
            <label className="block mb-1 text-sm text-gray-300" htmlFor="valor-input">Valor Desejado (R$):</label>
            <input
              id="valor-input"
              type="text"
              value={valor}
              onChange={handleChangeValor}
              className="w-full px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-600 focus:outline-none focus:border-orange-500"
              placeholder="Ex: R$ 15.000,00"
            />
          </div>

          <div className="mb-4">
            <label className="block mb-1 text-sm text-gray-300" htmlFor="prazo-input">
              Prazo (em meses):
            </label>
            <input
              id="prazo-input"
              type="number"
              value={prazo}
              onChange={(e) => setPrazo(parseInt(e.target.value))}
              min="6"
              max="60"
              className="w-full px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-600 focus:outline-none focus:border-orange-500 appearance-none [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none [-moz-appearance:textfield]"
              placeholder="Ex: 24"
            />
          </div>

          <div className="mb-6">
            <label className="block mb-1 text-sm text-gray-300" htmlFor="finalidade-input">Finalidade:</label>
            <input
              id="finalidade-input"
              type="text"
              value={finalidade}
              onChange={(e) => setFinalidade(e.target.value)}
              className="w-full px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-600 focus:outline-none focus:border-orange-500"
              placeholder="Ex: Reforma da casa"
            />
          </div>

          <div className="flex justify-center">
            <button
              onClick={handleSubmit}
              className="px-8 py-3 bg-orange-600 hover:bg-orange-700 text-white font-semibold rounded-lg shadow-md transition duration-300 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-opacity-75"
            >
              Solicitar Empréstimo
            </button>
          </div>
        </>
      )}

      {mensagem && (
        <p className="mt-4 text-center text-green-500 font-medium">{mensagem}</p>
      )}
      {erro && (
        <p className="mt-4 text-center text-red-500 font-medium">{erro}</p>
      )}
    </div>
  );
}

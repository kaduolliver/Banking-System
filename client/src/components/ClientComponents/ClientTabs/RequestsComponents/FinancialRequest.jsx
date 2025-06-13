import { useState } from "react";
import { useAuth } from '../../../../context/authContext';
//import { solicitarEmprestimo } from '../../../../services/cliente/emprestimoService';

export default function FinancialRequest() {
  const { usuario } = useAuth();

  const [valor, setValor] = useState("");
  const [prazo, setPrazo] = useState(12);
  const [finalidade, setFinalidade] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [erro, setErro] = useState("");

  const validarDados = () => {
    const valorNum = parseFloat(valor);
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
    return true;
  };

  const handleSubmit = async () => {
    if (!validarDados()) return;

    try {
      await solicitarEmprestimo({
        id_usuario: usuario.id_usuario,
        valor_solicitado: parseFloat(valor),
        prazo_meses: prazo,
        finalidade: finalidade.trim(),
      });

      setMensagem("Solicitação de empréstimo enviada com sucesso!");
      setErro("");
      setValor("");
      setPrazo(12);
      setFinalidade("");
    } catch (e) {
      setErro(e.message || "Erro ao solicitar empréstimo.");
      setMensagem("");
    }
  };

  return (
    <div className="p-6 bg-gray-900 rounded-xl shadow-md">
      <h3 className="text-xl font-semibold mb-4 text-orange-400 text-center">
        Solicitar Empréstimo
      </h3>

      <div className="mb-4">
        <label className="block mb-1 text-sm text-gray-300">Valor Desejado (R$):</label>
        <input
          type="number"
          value={valor}
          onChange={(e) => setValor(e.target.value)}
          min="1000"
          max="100000"
          className="w-full px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-600"
          placeholder="Ex: 15000"
        />
      </div>

      <div className="mb-4">
        <label className="block mb-1 text-sm text-gray-300">Prazo (em meses):</label>
        <input
          type="number"
          value={prazo}
          onChange={(e) => setPrazo(parseInt(e.target.value))}
          min="6"
          max="60"
          className="w-full px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-600"
          placeholder="Ex: 24"
        />
      </div>

      <div className="mb-4">
        <label className="block mb-1 text-sm text-gray-300">Finalidade:</label>
        <input
          type="text"
          value={finalidade}
          onChange={(e) => setFinalidade(e.target.value)}
          className="w-full px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-600"
          placeholder="Ex: Reforma da casa"
        />
      </div>

      <div className="flex justify-center">
        <button
          onClick={handleSubmit}
          className="px-6 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-lg transition"
        >
          Solicitar Empréstimo
        </button>
      </div>

      {mensagem && (
        <p className="mt-4 text-center text-green-500 font-medium">{mensagem}</p>
      )}
      {erro && (
        <p className="mt-4 text-center text-red-500 font-medium">{erro}</p>
      )}
    </div>
  );
}

import { useState, useEffect } from "react";
import { useAuth } from "../../../../context/authContext";
import { verificarConta, solicitarAberturaConta } from '../../../../services/cliente/contaService';

export default function FinancialServices() {
    const { usuario, carregando } = useAuth();
    const [temConta, setTemConta] = useState(null);
    const [mensagem, setMensagem] = useState("");
    const [erro, setErro] = useState("");
    const [tipoConta, setTipoConta] = useState("corrente");

    useEffect(() => {
        const checarConta = async () => {
            try {
                const existeConta = await verificarConta(usuario.id_usuario);
                setTemConta(existeConta);
            } catch {
                setErro("Erro ao verificar conta. Tente novamente.");
                setTemConta(false);
            }
        };

        if (usuario?.id_usuario) checarConta();
    }, [usuario]);

    const handleSolicitacao = async () => {
        try {
            await solicitarAberturaConta(usuario.id_usuario, tipoConta);
            setMensagem("Solicitação enviada com sucesso.");
            setErro("");
        } catch (e) {
            setMensagem("");
            setErro(e.message || "Erro ao enviar solicitação.");
        }
    };

    if (carregando) {
        return <p className="text-center text-gray-600">Carregando sessão...</p>;
    }

    return (
        <div className="max-w-xl mx-auto mt-10 p-6 bg-black shadow-lg rounded-2xl">
            <h2 className="text-2xl font-semibold mb-4 text-center text-gray-200">
                Serviços Financeiros
            </h2>

            {temConta === null ? (
                <p className="text-gray-600 text-center">Verificando sua conta...</p>
            ) : temConta ? (
                <p className="text-green-600 text-center">
                    Você já possui uma conta ativa.
                </p>
            ) : (
                <>
                    <p className="text-red-600 mb-4 text-center">
                        Você ainda não possui uma conta. Deseja solicitar a abertura?
                    </p>

                    <div className="mb-4 text-center">
                        <label className="block text-gray-200 mb-2">Tipo de Conta:</label>
                        <select
                            value={tipoConta}
                            onChange={(e) => setTipoConta(e.target.value)}
                            className="w-64 px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-600"
                        >
                            <option value="corrente">Conta Corrente</option>
                            <option value="poupanca">Conta Poupança</option>
                            <option value="investimento">Conta Investimento</option>
                        </select>
                    </div>

                    <div className="flex justify-center">
                        <button
                            onClick={handleSolicitacao}
                            className="px-6 py-2 bg-gradient-to-r from-amber-600 to-orange-700 hover:from-orange-700 hover:to-amber-600 text-white rounded-lg transition"
                        >
                            Solicitar Abertura
                        </button>
                    </div>
                </>
            )}

            {mensagem && (
                <p className="mt-4 text-center font-medium text-green-500">{mensagem}</p>
            )}
            {erro && (
                <p className="mt-4 text-center font-medium text-red-500">{erro}</p>
            )}
        </div>
    );
}

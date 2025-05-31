import { useState, useEffect } from "react";
import { verificarConta, solicitarAberturaConta } from "../../services/cliente/contaService";

export default function FinancialServices() {
    const [temConta, setTemConta] = useState(null);
    const [mensagem, setMensagem] = useState("");
    const [erro, setErro] = useState("");

    useEffect(() => {
        const checarConta = async () => {
            try {
                const existeConta = await verificarConta();
                setTemConta(existeConta);
            } catch (err) {
                setErro("Erro ao verificar conta. Tente novamente mais tarde.");
                setTemConta(false);
            }
        };

        checarConta();
    }, []);

    const handleSolicitacao = async () => {
        try {
            await solicitarAberturaConta();
            setMensagem("Solicitação enviada com sucesso.");
        } catch (err) {
            setMensagem("Erro ao enviar solicitação.");
        }
    };

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
                    <div className="flex justify-center">
                        <button
                            onClick={handleSolicitacao}
                            className="px-6 py-2 bg-gradient-to-r from-amber-600 to-orange-700 hover:from-orange-700 hover:to-amber-600 text-white rounded-lg transition"
                        >
                            Solicitar Abertura de Conta
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

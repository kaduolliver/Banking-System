import { useAuth } from '../../context/authContext';
import { formatCPF, formatData, formatTelefone, capitalize } from '../Common/formatters';
import { atualizarTelefone } from '../../services/auth/userService';
import { useState } from 'react';

export default function ClientPersonalData() {
    const { usuario, carregando } = useAuth();
    const [telefone, setTelefone] = useState(usuario?.telefone || '');
    const [editando, setEditando] = useState(false);
    const [loading, setLoading] = useState(false);
    const [erro, setErro] = useState(null);

    if (carregando) return <div className="text-zinc-400">Carregando...</div>;
    if (!usuario) return <div className="text-red-400">Usuário não autenticado.</div>;

    async function salvarTelefone() {
        setLoading(true);
        setErro(null);
        try {
            await atualizarTelefone(telefone);
            setEditando(false);
            // Você pode também atualizar o contexto aqui se quiser refletir a mudança imediatamente
        } catch (e) {
            setErro(e.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="flex justify-center relative top-5">
            <div className="w-full max-w-3xl space-y-6">
                <h2 className="text-2xl font-semibold text-white border-b border-zinc-700 pb-2">
                    Dados Pessoais
                </h2>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                    <InfoItem label="Nome" value={usuario.nome} />
                    <InfoItem label="CPF" value={formatCPF(usuario.cpf)} />
                    <div>
                        <div className="text-sm text-zinc-400">Telefone</div>
                        {editando ? (
                            <>
                                <input
                                    type="text"
                                    className="w-full p-2 rounded bg-zinc-800 text-white"
                                    value={telefone}
                                    onChange={e => setTelefone(e.target.value)}
                                />
                                <button
                                    disabled={loading}
                                    onClick={salvarTelefone}
                                    className="mt-2 px-4 py-1 bg-blue-600 rounded text-white hover:bg-blue-700"
                                >
                                    {loading ? 'Salvando...' : 'Salvar'}
                                </button>
                                <button
                                    disabled={loading}
                                    onClick={() => {
                                        setTelefone(usuario.telefone);
                                        setEditando(false);
                                        setErro(null);
                                    }}
                                    className="ml-2 mt-2 px-4 py-1 bg-gray-600 rounded text-white hover:bg-gray-700"
                                >
                                    Cancelar
                                </button>
                                {erro && <div className="text-red-500 mt-1">{erro}</div>}
                            </>
                        ) : (
                            <>
                                <div className="text-base text-white font-medium">{formatTelefone(telefone)}</div>
                                <button
                                    onClick={() => setEditando(true)}
                                    className="mt-1 text-sm text-blue-400 underline"
                                >
                                    Editar
                                </button>
                            </>
                        )}
                    </div>
                    <InfoItem label="Tipo de Usuário" value={capitalize(usuario.tipo_usuario)} />
                    <InfoItem label="Data de Nascimento" value={formatData(usuario.data_nascimento)} />
                </div>
            </div>
        </div>
    );
}

function InfoItem({ label, value }) {
    return (
        <div className="space-y-1">
            <div className="text-sm text-zinc-400">{label}</div>
            <div className="text-base text-white font-medium">{value}</div>
        </div>
    );
}

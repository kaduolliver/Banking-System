import { useState, useEffect } from 'react';
import { Edit2 } from 'lucide-react';
import { InputMask } from '@react-input/mask';
import StateSelect from '../../../../Common/StateSelect';
import {
    buscarEnderecoAgencia,
    cadastrarEnderecoAgencia,
    atualizarEnderecoAgencia,
} from '../../../../services/agency/agencyService';
import { useAuth } from '../../../../context/authContext';
import { formatCEP } from '../../../../utils/formatters';

export default function AgencyAddressForm({ onEnderecoSalvo }) {
    const { usuario, carregando, atualizarUsuario } = useAuth();

    const [endereco, setEndereco] = useState(null);
    const [novoEndereco, setNovoEndereco] = useState({});
    const [editandoEndereco, setEditandoEndereco] = useState(false);
    const [carregandoEndereco, setCarregandoEndereco] = useState(true);
    const [loading, setLoading] = useState(false);
    const [erro, setErro] = useState(null);

    const agenciaId = usuario?.tipo_usuario === 'funcionario' ? usuario.id_agencia : null;
    const isAdministrador = usuario?.tipo_usuario === 'funcionario' && (usuario?.cargo === 'Admin');

    useEffect(() => {
        async function fetchEndereco() {
            try {
                const data = await buscarEnderecoAgencia(agenciaId);
                const enderecoRecebido = Array.isArray(data) ? data[0] : data;

                if (enderecoRecebido && enderecoRecebido.cep) {
                    const cepFormatado = formatCEP(enderecoRecebido.cep);
                    setEndereco(enderecoRecebido);
                    setNovoEndereco({ ...enderecoRecebido, cep: cepFormatado });

                } else {
                    setEndereco(null);
                    setNovoEndereco({
                        cep: '', logradouro: '', numero_casa: '', bairro: '', estado: '', complemento: '',
                    });
                }
            } catch (e) {
                setErro('Erro ao carregar endereço da agência.');
            } finally {
                setCarregandoEndereco(false);
            }
        }

        if (agenciaId && !usuario?.endereco_agencia) {
            fetchEndereco();
        } else if (usuario?.endereco_agencia) {
            const enderecoUsuario = usuario.endereco_agencia;
            const cepFormatado = formatCEP(enderecoUsuario.cep);
            setEndereco(enderecoUsuario);
            setNovoEndereco({ ...enderecoUsuario, cep: cepFormatado });
            setCarregandoEndereco(false);
        }
    }, [agenciaId]);

    function handleChange(e) {
        const { name, value } = e.target;
        setNovoEndereco(prev => ({ ...prev, [name]: value }));
        setErro(null);
    }

    async function salvarEndereco() {
        const { cep, logradouro, numero_casa, bairro, estado } = novoEndereco;
        if (!cep || !logradouro || !numero_casa || !bairro || !estado) {
            setErro('Preencha todos os campos obrigatórios.');
            return;
        }

        setLoading(true);
        try {
            const enderecoEnviado = { ...novoEndereco, cep: novoEndereco.cep.replace(/\D/g, '') };
            let resultado;

            if (endereco?.id_endereco) {
                resultado = await atualizarEnderecoAgencia(agenciaId, enderecoEnviado);
            } else {
                resultado = await cadastrarEnderecoAgencia(agenciaId, enderecoEnviado);
            }

            atualizarUsuario({ endereco_agencia: resultado });
            setEndereco(resultado);
            setNovoEndereco(resultado);
            setEditandoEndereco(false);
            setErro(null);
            if (onEnderecoSalvo) onEnderecoSalvo(resultado);
        } catch (e) {
            setErro(e.message || 'Erro ao salvar endereço.');
        } finally {
            setLoading(false);
        }
    }

    if (carregando || carregandoEndereco) return <div className="text-zinc-400">Carregando endereço...</div>;

    return (
        <div className="w-full max-w-3xl mx-auto space-y-6 mt-6">
            <h2 className="text-2xl font-semibold text-white border-b border-zinc-700 pb-2 flex justify-between">
                Endereço da Agência
                {!editandoEndereco && isAdministrador && (
                    <button
                        onClick={() => {
                            setNovoEndereco(endereco || {
                                cep: '', estado: '', logradouro: '', numero_casa: '', bairro: '', complemento: '',
                            });
                            setEditandoEndereco(true);
                            setErro(null);
                        }}
                        title={endereco ? "Editar Endereço" : "Adicionar Endereço"}
                    >
                        <Edit2 className="text-amber-600 hover:text-amber-200" size={20} />
                    </button>
                )}
            </h2>

            {!isAdministrador && (
                <div className="text-red-400 text-sm mt-1">Você não tem permissão para editar o endereço da agência.</div>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {['cep', 'estado', 'logradouro', 'numero_casa', 'bairro', 'complemento'].map(campo => (
                    <div key={campo} className="flex flex-col">
                        <label className="text-sm text-zinc-400">{campo.replace('_', ' ').toUpperCase()}</label>
                        {campo === 'cep' ? (
                            <InputMask
                                mask="_____-___"
                                replacement={{ _: /\d/ }}
                                name="cep"
                                value={novoEndereco.cep || ''}
                                onChange={handleChange}
                                className={`w-full p-2 rounded bg-zinc-800 text-white outline-none ${editandoEndereco ? 'border border-amber-600' : 'opacity-70'}`}
                                placeholder="00000-000"
                                disabled={!editandoEndereco}
                            />
                        ) : campo === 'estado' ? (
                            <StateSelect
                                name="estado"
                                value={novoEndereco.estado || ''}
                                onChange={handleChange}
                                className={`w-full p-2 rounded bg-zinc-800 text-white outline-none ${editandoEndereco ? 'border border-amber-600' : 'opacity-70'}`}
                                disabled={!editandoEndereco}
                            />
                        ) : (
                            <input
                                name={campo}
                                value={novoEndereco[campo] || ''}
                                onChange={handleChange}
                                placeholder={campo === 'complemento' ? 'Apartamento, Casa, etc.' : ''}
                                className={`w-full p-2 rounded bg-zinc-800 text-white outline-none ${editandoEndereco ? 'border border-amber-600' : 'opacity-70'}`}
                                disabled={!editandoEndereco}
                            />
                        )}
                    </div>
                ))}
            </div>

            {erro && <div className="text-red-500">{erro}</div>}

            {editandoEndereco && (
                <div className="flex gap-3 mt-2">
                    <button
                        onClick={salvarEndereco}
                        disabled={loading}
                        className="px-4 py-2 bg-amber-700 hover:bg-amber-600 text-white rounded"
                    >
                        {loading ? 'Salvando...' : 'Salvar'}
                    </button>
                    <button
                        onClick={() => {
                            setNovoEndereco(endereco || {});
                            setEditandoEndereco(false);
                            setErro(null);
                        }}
                        disabled={loading}
                        className="px-4 py-2 bg-gray-600 hover:bg-gray-500 text-white rounded"
                    >
                        Cancelar
                    </button>
                </div>
            )}
        </div>
    );
}

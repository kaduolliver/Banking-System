import * as Tabs from '@radix-ui/react-tabs';
import { motion } from 'framer-motion';
import { useState } from 'react';

const tiposConta = ['poupanca', 'corrente', 'investimento'];

export default function ClientAccountData({ dadosConta }) {
    const [tipoSelecionado, setTipoSelecionado] = useState('poupanca');

    if (!dadosConta) return <div className="text-red-400">Conta não encontrada.</div>;

    const { agencia, numero, contas } = dadosConta;

    return (
        <div className="flex justify-center mt-6">
            <div className="w-full max-w-3xl space-y-6">
                <h2 className="text-2xl font-semibold text-white border-b border-zinc-700 pb-2">Dados da Conta</h2>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                    <InfoItem label="Agência" value={agencia} />
                    <InfoItem label="Número da Conta" value={numero} />
                </div>

                <Tabs.Root value={tipoSelecionado} onValueChange={setTipoSelecionado}>
                    <Tabs.List className="flex space-x-4 mt-6">
                        {tiposConta.map(tipo => (
                            <Tabs.Trigger
                                key={tipo}
                                value={tipo}
                                className={`px-4 py-1 rounded font-medium ${
                                    tipoSelecionado === tipo
                                        ? 'bg-amber-700 text-white cursor-default'
                                        : 'bg-zinc-800 text-zinc-300 hover:bg-zinc-700'
                                }`}
                                disabled={tipoSelecionado === tipo}
                            >
                                {tipo.charAt(0).toUpperCase() + tipo.slice(1)}
                            </Tabs.Trigger>
                        ))}
                    </Tabs.List>

                    <div className="relative mt-6">
                        <Tabs.Content value="poupanca" asChild>
                            <motion.div
                                key="poupanca"
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: 20 }}
                                className="grid grid-cols-1 sm:grid-cols-2 gap-6"
                            >
                                <InfoItem label="Taxa de Rendimento" value={formatPorcentagem(contas.poupanca?.taxa_rendimento)} />
                                <InfoItem label="Último Rendimento" value={formatMoeda(contas.poupanca?.ultimo_rendimento)} />
                            </motion.div>
                        </Tabs.Content>

                        <Tabs.Content value="corrente" asChild>
                            <motion.div
                                key="corrente"
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: 20 }}
                                className="grid grid-cols-1 sm:grid-cols-2 gap-6"
                            >
                                <InfoItem label="Limite" value={formatMoeda(contas.corrente?.limite)} />
                                <InfoItem label="Data de Vencimento" value={formatData(contas.corrente?.data_vencimento)} />
                                <InfoItem label="Taxa de Manutenção" value={formatPorcentagem(contas.corrente?.taxa_manutencao)} />
                            </motion.div>
                        </Tabs.Content>

                        <Tabs.Content value="investimento" asChild>
                            <motion.div
                                key="investimento"
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: 20 }}
                                className="grid grid-cols-1 sm:grid-cols-2 gap-6"
                            >
                                <InfoItem label="Perfil de Risco" value={capitalize(contas.investimento?.perfil_risco)} />
                                <InfoItem label="Valor Mínimo" value={formatMoeda(contas.investimento?.valor_minimo)} />
                                <InfoItem label="Taxa Rendimento Base" value={formatPorcentagem(contas.investimento?.taxa_rendimento_base)} />
                            </motion.div>
                        </Tabs.Content>
                    </div>
                </Tabs.Root>
            </div>
        </div>
    );
}

function InfoItem({ label, value }) {
    return (
        <div className="space-y-1">
            <div className="text-sm text-zinc-400">{label}</div>
            <div className="text-base text-white font-medium">{value ?? '—'}</div>
        </div>
    );
}

function formatMoeda(valor) {
    if (valor == null) return '—';
    return Number(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function formatPorcentagem(valor) {
    if (valor == null) return '—';
    return `${(valor * 100).toFixed(2)}%`;
}

function formatData(data) {
    if (!data) return '—';
    return new Date(data).toLocaleDateString('pt-BR');
}

function capitalize(texto) {
    if (!texto) return '—';
    return texto.charAt(0).toUpperCase() + texto.slice(1).toLowerCase();
}

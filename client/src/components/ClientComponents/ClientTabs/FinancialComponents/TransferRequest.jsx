import { useState } from "react";

export default function TransferRequest() {
  const [amount, setAmount] = useState("");
  const [targetAccount, setTargetAccount] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState("");

  const saldo = 500; // Exemplo de saldo atual

  const handleSubmit = async (e) => {
    e.preventDefault();
    const valor = parseFloat(amount);

    if (isNaN(valor) || valor < 10) {
      setError("Valor mínimo para transferência é R$ 10");
      setSuccess("");
      return;
    }
    if (valor > saldo) {
      setError("Saldo insuficiente para este valor");
      setSuccess("");
      return;
    }
    if (!targetAccount.match(/^\d{6,}$/)) {
      setError("Conta destino inválida (mínimo 6 dígitos numéricos)");
      setSuccess("");
      return;
    }

    setError("");
    setLoading(true);
    setSuccess("");

    await new Promise((r) => setTimeout(r, 1500)); // simula API

    setLoading(false);
    setSuccess(`Transferência de R$ ${valor.toFixed(2)} para conta ${targetAccount} realizada com sucesso!`);
    setAmount("");
    setTargetAccount("");
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="grid grid-cols-1 sm:grid-cols-2 gap-6 text-white"
      aria-live="polite"
    >
      <div className="sm:col-span-2">
        <p className="text-sm text-zinc-400 font-medium mb-2">
          Saldo disponível:{" "}
          <span className="text-green-400 font-semibold">R$ {saldo.toFixed(2)}</span>
        </p>
      </div>

      <FormItem label="Conta Destino">
        <input
          id="transfer-account"
          type="text"
          value={targetAccount}
          onChange={(e) => setTargetAccount(e.target.value)}
          required
          disabled={loading}
          placeholder="Digite o número da conta"
          aria-invalid={!!(error && !targetAccount)}
          className={`w-full px-3 py-2 rounded bg-zinc-800 text-white border focus:outline-none focus:ring-2 focus:ring-amber-600 transition ${
            error && !targetAccount ? "border-red-500" : "border-zinc-700"
          }`}
        />
      </FormItem>

      <FormItem label="Valor para Transferência">
        <input
          id="transfer-amount"
          type="number"
          min="0.01"
          step="0.01"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
          disabled={loading}
          placeholder="Digite o valor"
          aria-invalid={!!(error && amount)}
          className={`w-full px-3 py-2 rounded bg-zinc-800 text-white border focus:outline-none focus:ring-2 focus:ring-amber-600 transition [&::-webkit-outer-spin-button]:appearance-none
            [&::-webkit-inner-spin-button]:appearance-none
            [appearance:textfield] ${
            error && amount ? "border-red-500" : "border-zinc-700"
          }`}
        />
      </FormItem>

      {error && (
        <div className="sm:col-span-2">
          <p role="alert" className="text-sm text-red-500 font-semibold mt-1">{error}</p>
        </div>
      )}

      <div className="sm:col-span-2">
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2 bg-gradient-to-r from-amber-600 to-orange-700 hover:from-orange-700 hover:to-amber-600 text-white rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "Enviando..." : "Solicitar Transferência"}
        </button>

        {success && (
          <p role="status" className="mt-2 text-green-500 font-medium text-sm">{success}</p>
        )}
      </div>
    </form>
  );
}

function FormItem({ label, children }) {
  return (
    <div className="space-y-1">
      <div className="text-sm text-zinc-400">{label}</div>
      {children}
    </div>
  );
}

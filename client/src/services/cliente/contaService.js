export async function verificarConta() {
  const id_usuario = localStorage.getItem("id_usuario");
  const res = await fetch(`/api/cliente/verificar-conta/${id_usuario}`);
  if (!res.ok) throw new Error("Erro ao verificar conta");
  return (await res.json()).temConta;
}

export async function solicitarAberturaConta() {
  const id_usuario = localStorage.getItem("id_usuario");
  const res = await fetch("/api/cliente/solicitar-conta", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id_usuario }),
  });
  if (!res.ok) throw new Error("Erro ao solicitar conta");
  return true;
}

export function formatCPF(cpf) {
  if (!cpf) return '';
  cpf = cpf.replace(/\D/g, '');
  return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

export function formatTelefone(telefone) {
  if (!telefone) return '';
  telefone = telefone.replace(/\D/g, '');
  if (telefone.length === 11) {
    return telefone.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
  } else if (telefone.length === 10) {
    return telefone.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
  }
  return telefone;
}

export function formatData(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  const day = String(date.getUTCDate()).padStart(2, '0');
  const month = String(date.getUTCMonth() + 1).padStart(2, '0');
  const year = date.getUTCFullYear();
  return `${day}/${month}/${year}`;
};

export function capitalize(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function validarTelefone(telefone) {
  const regex = /^\(\d{2}\)\s\d{5}-\d{4}$/;
  return regex.test(telefone);
}

export function formatCEP(cep) {
    const digits = cep.replace(/\D/g, '');
    return digits.replace(/^(\d{5})(\d{3})$/, '$1-$2');
}

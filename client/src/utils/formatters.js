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
  if (!cep) return '';
  return cep
    .replace(/\D/g, '')
    .replace(/^(\d{5})(\d)/, '$1-$2')
    .slice(0, 9);
}

export function formatarMoeda(valor) {
  // Se o valor de entrada é realmente vazio, null ou undefined,
  // ou se após a limpeza de não-dígitos resulta em algo que não é número (e não é zero),
  // podemos retornar uma string vazia para limpar o campo.
  // Caso contrário, ele tentará formatar o '0' para 'R$ 0,00'.
  const valorApenasNumeros = valor.toString().replace(/[^\d]/g, "");
  
  if (valorApenasNumeros === "") {
      return ""; // Campo fica vazio se nada significativo foi digitado
  }

  const numeroCentavos = parseInt(valorApenasNumeros, 10);

  // Se parseInt falhar (ex: string com apenas letras após replace), ainda retorna vazio
  if (isNaN(numeroCentavos)) return ""; 

  const numeroReais = numeroCentavos / 100;

  return numeroReais.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
    minimumFractionDigits: 2,
  });
}

export function desformatarMoeda(valorFormatado) {
  // Se a entrada for vazia, null ou undefined, retorne 0 (número)
  // Isso permite que formatarMoeda formate "0" para "R$ 0,00"
  if (!valorFormatado) {
    return 0; // Importante retornar o número 0 aqui
  }

  const apenasNumeros = valorFormatado.replace(/[^\d,]/g, "");

  // Se após remover caracteres a string estiver vazia, significa que não havia números válidos,
  // então consideramos 0.
  if (apenasNumeros === "") {
    return 0; // Importante retornar o número 0 aqui
  }

  const valorComPonto = apenasNumeros.replace(/,/g, ".");

  const valorFloat = parseFloat(valorComPonto);

  // Se parseFloat resultar em NaN (ex: "."), retorne 0 para que o campo possa exibir "R$ 0,00"
  if (isNaN(valorFloat)) {
    return 0; // Importante retornar o número 0 aqui
  }

  return valorFloat;
}

export function corDoScore(valor) {
  if (valor == null) return 'text-white';            
  if (valor <= 39) return 'text-red-500';            
  if (valor <= 79) return 'text-yellow-400';         
  return 'text-green-500';                           
}

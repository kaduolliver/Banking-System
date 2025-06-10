import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { UserPlus } from 'lucide-react';
import FormContainer from './LoginFormComponents/FormContainer';
import InputField from './LoginFormComponents/InputField';
import PasswordField from './LoginFormComponents/PasswordField';
import PasswordCriteria from './LoginFormComponents/PasswordCriteria';
import { registerUsuario } from '../../services/auth/registerService';
import { getAgencias } from '../../services/agency/agencyService'

export default function RegisterUser({ onToggle }) {
  const [formData, setFormData] = useState({
    nome: '',
    cpf: '',
    data_nascimento: '',
    telefone: '',
    tipo_usuario: 'cliente',
    senha: '',
    confirmarSenha: '',
    id_agencia: '',
  });

  const [erroSenha, setErroSenha] = useState('');
  const [erroGeral, setErroGeral] = useState(''); // Novo estado para erros gerais da API
  const [agencias, setAgencias] = useState([]); // <-- Novo estado para armazenar as agências
  const [isLoadingAgencias, setIsLoadingAgencias] = useState(false); // Para controle de loading das agências

  const passwordCriteria = {
    comprimento: {
      label: 'Mínimo de 8 caracteres',
      test: (s) => s.length >= 8,
    },
    maiuscula: {
      label: 'Letra maiúscula (A-Z)',
      test: (s) => /[A-Z]/.test(s),
    },
    minuscula: {
      label: 'Letra minúscula (a-z)',
      test: (s) => /[a-z]/.test(s),
    },
    numero: {
      label: 'Número (0-9)',
      test: (s) => /[0-9]/.test(s),
    },
    especial: {
      label: 'Caractere especial (!@#$...)',
      test: (s) => /[!@#$%^&*(),.?":{}|<>]/.test(s),
    },
  };

  const isSenhaValida = () =>
    Object.values(passwordCriteria).every((crit) => crit.test(formData.senha));

  // --- Efeito para carregar as agências ao montar o componente ---
  useEffect(() => {
    async function fetchAgencias() {
      setIsLoadingAgencias(true);
      try {
        const response = await getAgencias(); // <--- Chame o serviço para buscar agências
        setAgencias(response); // Assumindo que response é um array de agências
      } catch (error) {
        setErroGeral('Erro ao carregar agências. Tente novamente mais tarde.');
        console.error('Erro ao buscar agências:', error);
      } finally {
        setIsLoadingAgencias(false);
      }
    }
    fetchAgencias();
  }, []); // Array de dependências vazio para rodar apenas uma vez

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setErroSenha('');
    setErroGeral(''); // Limpa erro geral ao mudar algo
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isSenhaValida()) {
      setErroSenha('A senha não atende aos critérios obrigatórios.');
      return;
    }

    if (formData.senha !== formData.confirmarSenha) {
      setErroSenha('As senhas não coincidem.');
      return;
    }

    // --- Validação para funcionário e agência ---
    if (formData.tipo_usuario === 'funcionario' && !formData.id_agencia) {
      setErroGeral('Por favor, selecione a agência para o funcionário.');
      return;
    }
    // --- Fim da validação ---

    setErroSenha('');
    setErroGeral(''); // Limpa erros antes de tentar submeter

    const dadosLimpos = {
      ...formData,
      cpf: formData.cpf.replace(/\D/g, ''),
      telefone: formData.telefone.replace(/\D/g, ''),
    };

    // --- Remover id_agencia se o tipo for cliente ---
    if (dadosLimpos.tipo_usuario === 'cliente') {
      delete dadosLimpos.id_agencia;
    } else {
      // Garante que id_agencia seja um número
      dadosLimpos.id_agencia = parseInt(dadosLimpos.id_agencia, 10);
    }
    // --- Fim da remoção condicional ---

    try {
      const data = await registerUsuario(dadosLimpos);
      alert("Registro realizado com sucesso!");
      setFormData({ // Limpa o formulário
        nome: '', cpf: '', data_nascimento: '', telefone: '',
        tipo_usuario: 'cliente', senha: '', confirmarSenha: '', id_agencia: '',
      });
      window.scrollTo({ top: 0, behavior: 'smooth' });
      onToggle(); // Volta para a tela de login
    } catch (error) {
      setErroGeral(error.message || 'Erro ao registrar usuário.');
      console.error('Erro de registro:', error);
    }
  };

  return (
    <FormContainer
      onSubmit={handleSubmit}
      title="Crie sua conta"
      icon={<UserPlus className="text-amber-600" />}
    >
      <InputField label="Nome completo" name="nome" value={formData.nome} onChange={handleChange} />

      <div className="grid grid-cols-1 md:grid-cols-7 gap-4">
        <div className="md:col-span-4">
          <InputField
            label="CPF"
            name="cpf"
            value={formData.cpf}
            onChange={handleChange}
            mask="___.___.___-__"
          />
        </div>
        <div className="md:col-span-3">
          <InputField
            label="Nascimento"
            name="data_nascimento"
            value={formData.data_nascimento}
            onChange={handleChange}
            type="date"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-7 gap-4 mt-4">
        <div className="md:col-span-4">
          <InputField
            label="Telefone"
            name="telefone"
            value={formData.telefone}
            onChange={handleChange}
            mask="(__) _____-____"
            icon="phone" // Supondo que 'phone' seja um tipo de ícone reconhecido pelo InputField
          />
        </div>
        <div className="md:col-span-3">
          <label htmlFor="tipo_usuario" className="block text-sm font-medium mb-1 dark:text-gray-300">
            Tipo de Usuário
          </label>
          <select
            id="tipo_usuario"
            name="tipo_usuario"
            value={formData.tipo_usuario}
            onChange={handleChange}
            className="w-full p-2 border dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 dark:text-white focus:ring-2 focus:ring-amber-600"
          >
            <option value="cliente">Cliente</option>
            <option value="funcionario">Funcionário</option>
          </select>
        </div>
      </div>

      {/* --- Novo campo de seleção de agência, condicional --- */}
      {formData.tipo_usuario === 'funcionario' && (
        <div className="relative">
          <label htmlFor="id_agencia" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Agência
          </label>
          {isLoadingAgencias ? (
            <p className="text-gray-500 dark:text-gray-400">Carregando agências...</p>
          ) : (
            <select
              id="id_agencia"
              name="id_agencia"
              value={formData.id_agencia}
              onChange={handleChange}
              className="w-full p-2 border dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 dark:text-white focus:ring-2 focus:ring-amber-600"
            >
              <option value="">Selecione uma agência</option>
              {agencias.map((agencia) => (
                <option key={agencia.id_agencia} value={agencia.id_agencia}>
                  {agencia.nome} ({agencia.codigo_agencia})
                </option>
              ))}
            </select>
          )}
        </div>
      )}
      {/* --- Fim do novo campo --- */}

      <PasswordField label="Senha" name="senha" value={formData.senha} onChange={handleChange} />
      <PasswordField label="Confirmar Senha" name="confirmarSenha" value={formData.confirmarSenha} onChange={handleChange} />

      <PasswordCriteria senha={formData.senha} criteria={passwordCriteria} />

      {(erroSenha || erroGeral) && ( // Exibir erro de senha ou erro geral
        <motion.p
          className="text-red-600 text-sm font-medium"
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
        >
          {erroSenha || erroGeral}
        </motion.p>
      )}

      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.96 }}
        type="submit"
        className="w-full bg-gradient-to-r from-amber-600 to-orange-700 hover:from-orange-700 hover:to-amber-600 text-white py-2 px-4 rounded-2xl shadow-lg transition-all duration-300 font-semibold"
      >
        Cadastrar
      </motion.button>

      <p className="text-sm mt-2 text-center text-gray-600 dark:text-gray-400">
        Já tem uma conta?{' '}
        <button
          type="button"
          onClick={() => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            onToggle();
          }}
          className="text-orange-700 hover:underline font-medium"
        >
          Fazer login
        </button>
      </p>
    </FormContainer>
  );
}
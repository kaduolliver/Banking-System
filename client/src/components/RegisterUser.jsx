import { useState } from 'react';
import { motion } from 'framer-motion';
import { UserPlus } from 'lucide-react';
import FormContainer from './LoginFormComponents/FormContainer';
import InputField from './LoginFormComponents/InputField';
import PasswordField from './LoginFormComponents/PasswordField';
import PasswordCriteria from './LoginFormComponents/PasswordCriteria';
import { registerUsuario } from '../services/auth/registerService';

export default function RegisterUser({ onToggle }) {
  const [formData, setFormData] = useState({
    nome: '',
    cpf: '',
    data_nascimento: '',
    telefone: '',
    tipo_usuario: 'cliente',
    senha: '',
    confirmarSenha: '',
  });

  const [erroSenha, setErroSenha] = useState('');

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

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (name === 'senha' || name === 'confirmarSenha') setErroSenha('');
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

    setErroSenha('');

    const dadosLimpos = {
      ...formData,
      cpf: formData.cpf.replace(/\D/g, ''),
      telefone: formData.telefone.replace(/\D/g, '')
    };

    try {
      const data = await registerUsuario(dadosLimpos);
      alert("Registro realizado com sucesso!");
    } catch (error) {
      alert("Erro ao registrar: " + error.message);
    }
  };

  return (
    <FormContainer
      onSubmit={handleSubmit}
      title="Crie sua conta"
      icon={<UserPlus className="text-amber-600" />}
    >
      <InputField label="Nome completo" name="nome" value={formData.nome} onChange={handleChange} />

      <div className="grid grid-cols-7 gap-4">
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

      <div className="grid grid-cols-7 gap-4 mt-4">
        <div className="md:col-span-4">
          <InputField
            label="Telefone"
            name="telefone"
            value={formData.telefone}
            onChange={handleChange}
            mask="(__) _____-____"
            icon="phone"
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

      <PasswordField label="Senha" name="senha" value={formData.senha} onChange={handleChange} />
      <PasswordField label="Confirmar Senha" name="confirmarSenha" value={formData.confirmarSenha} onChange={handleChange} />

      <PasswordCriteria senha={formData.senha} criteria={passwordCriteria} />

      {erroSenha && (
        <motion.p
          className="text-red-600 text-sm font-medium"
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
        >
          {erroSenha}
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
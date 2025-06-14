import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import RegisterUser from './RegisterUser';
import FormContainer from './LoginFormComponents/FormContainer';
import InputField from './LoginFormComponents/InputField';
import PasswordField from './LoginFormComponents/PasswordField';
import { User } from 'lucide-react';
import { LoginUsuario, VerificaOTP } from '../../services/auth/loginService';
import { useAuth } from '../../context/authContext';
import { useNavigate } from 'react-router-dom';
import SplashScreen from '../EffectsComponents/SplashScreen';

export default function LoginAndRegister() {
  const [modo, setModo] = useState('login');
  const [formData, setFormData] = useState({ usuario: '', senha: '', otp: '' });
  const [erro, setErro] = useState('');
  const [precisaOTP, setPrecisaOTP] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showSplash, setShowSplash] = useState(false);
  const [redirectPath, setRedirectPath] = useState('');

  const { setUsuario } = useAuth();
  const navigate = useNavigate();

  const handleSplashComplete = () => {
    localStorage.removeItem('mostrandoSplash');
    if (redirectPath) {
      navigate(redirectPath);
    }
  };

  const exibirSplashERedirecionar = (resposta) => {

    setUsuario({
      id_usuario: resposta.id_usuario,
      tipo_usuario: resposta.tipo_usuario,
      nome: resposta.nome || '',
      cpf: resposta.cpf,
      telefone: resposta.telefone,
      data_nascimento: resposta.data_nascimento,
      cargo: resposta.cargo || '',
      id_funcionario: resposta.id_funcionario,
      status_funcionario: resposta.status_funcionario,
      id_agencia: resposta.id_agencia,
      nome_agencia: resposta.nome_agencia || '',
      codigo_agencia: resposta.codigo_agencia || '',
      endereco_agencia: resposta.endereco_agencia || null,
      contas: resposta.contas || [],
      solicitacoes_conta: resposta.solicitacoes_conta,
      emprestimos: resposta.emprestimos || [],
      score_credito: resposta.score_credito,
    });

    localStorage.setItem('usuarioId', resposta.id_usuario);
    localStorage.setItem('tipo', resposta.tipo_usuario);
    localStorage.setItem('mostrandoSplash', 'true');
    
    let path = '';
    switch (resposta.tipo_usuario) {
      case 'cliente':
        path = '/user/client';
        break;
      case 'funcionario':
        path = '/user/employee';
        break;
      default:
        path = '/';
    }


    setRedirectPath(path);
    setShowSplash(true);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setErro('');
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();

    if (!formData.usuario || !formData.senha) {
      setErro('Preencha CPF e senha.');
      return;
    }

    setIsLoading(true);
    try {
      const cpfLimpo = formData.usuario.replace(/\D/g, '');
      const resposta = await LoginUsuario({ cpf: cpfLimpo, senha: formData.senha });

      if (resposta.precisa_otp) {
        setPrecisaOTP(true);
        setErro('Insira o código OTP enviado para você.');
      } else {
        exibirSplashERedirecionar(resposta);
      }
    } catch (err) {
      setErro(err.message || 'Erro no login.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleOtpSubmit = async (e) => {
    e.preventDefault();

    if (!formData.otp) {
      setErro('Informe o código OTP.');
      return;
    }

    setIsLoading(true);
    try {
      const cpfLimpo = formData.usuario.replace(/\D/g, '');
      const resposta = await VerificaOTP({ cpf: cpfLimpo, otp: formData.otp });

      exibirSplashERedirecionar(resposta);
    } catch (err) {
      setErro(err.message || 'Código OTP inválido.');
    } finally {
      setIsLoading(false);
    }
  };

  if (showSplash) {
    return <SplashScreen onComplete={handleSplashComplete} />;
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className={`relative w-full ${modo === 'registro' ? 'max-w-2xl' : 'max-w-md'}`}>
        <AnimatePresence mode="wait">
          {modo === 'login' ? (
            <motion.div
              key="login"
              initial={{ opacity: 0, x: 100 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -100 }}
              transition={{ duration: 0.6, ease: 'easeInOut' }}
            >
              <FormContainer
                title="Acesse sua conta"
                onSubmit={precisaOTP ? handleOtpSubmit : handleLoginSubmit}
                icon={<User className="text-amber-600" />}
              >
                <InputField
                  label="CPF"
                  name="usuario"
                  mask="___.___.___-__"
                  value={formData.usuario}
                  onChange={handleChange}
                  icon={User}
                  disabled={precisaOTP}
                />
                {!precisaOTP && (
                  <PasswordField
                    label="Senha"
                    name="senha"
                    value={formData.senha}
                    onChange={handleChange}
                  />
                )}
                {precisaOTP && (
                  <InputField
                    label="Código OTP"
                    name="otp"
                    value={formData.otp}
                    onChange={handleChange}
                    maxLength={6}
                  />
                )}
                <AnimatePresence>
                  {erro && (
                    <motion.p
                      className="text-red-600 text-sm font-medium"
                      initial={{ opacity: 0, x: 100 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -100 }}
                      transition={{ duration: 0.6, ease: 'easeInOut' }}
                    >
                      {erro}
                    </motion.p>
                  )}
                </AnimatePresence>
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.96 }}
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-gradient-to-r from-amber-600 to-orange-700 hover:from-orange-700 hover:to-amber-600 text-white py-2 px-4 rounded-2xl shadow-lg transition-all duration-300 font-semibold"
                >
                  {precisaOTP ? 'Validar OTP' : 'Entrar'}
                </motion.button>
                {!precisaOTP && (
                  <p className="text-sm mt-4 text-center text-gray-600 dark:text-gray-400">
                    Não tem uma conta?{' '}
                    <button
                      onClick={() => {
                        setModo('registro');
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                      }}
                      className="text-orange-700 hover:underline font-medium"
                    >
                      Cadastre-se
                    </button>
                  </p>
                )}
              </FormContainer>
            </motion.div>
          ) : (
            <motion.div
              key="registro"
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 50 }}
              transition={{ duration: 0.4 }}
            >
              <RegisterUser onToggle={() => setModo('login')} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

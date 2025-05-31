import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import RegisterUser from './RegisterUser';
import FormContainer from './LoginFormComponents/FormContainer';
import InputField from './LoginFormComponents/InputField';
import PasswordField from './LoginFormComponents/PasswordField';
import { User } from 'lucide-react';

// Funções API fictícias, você implementa conforme seu backend
import { LoginUsuario, VerificaOTP } from '../services/auth/loginService';

export default function AuthPage() {
  const [modo, setModo] = useState('login');
  const [formData, setFormData] = useState({ usuario: '', senha: '', otp: '' });
  const [erro, setErro] = useState('');
  const [precisaOTP, setPrecisaOTP] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setErro('');
  };

  // Primeiro submit: CPF + senha
  const handleLoginSubmit = async (e) => {
    e.preventDefault();

    if (!formData.usuario || !formData.senha) {
      setErro('Preencha CPF e senha.');
      return;
    }

    setIsLoading(true);
    try {
      const cpfLimpo = formData.usuario.replace(/\D/g, '');  // remove tudo que não é dígito

      const resposta = await LoginUsuario({ cpf: cpfLimpo, senha: formData.senha });

      if (resposta.precisa_otp) {
        setPrecisaOTP(true);
        setErro('Insira o código OTP enviado para você.');
      } else {
        // Login completo, redireciona ou salva sessão
        alert('Login realizado com sucesso!');
        // TODO: salvar token/session e redirecionar
      }
    } catch (err) {
      setErro(err.message || 'Erro no login.');
    } finally {
      setIsLoading(false);
    }
  };

  // Segundo submit: enviar OTP
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

      localStorage.setItem('usuarioId', resposta.id_usuario);
      localStorage.setItem('tipo', resposta.tipo);

      window.location.href = '/user';

    } catch (err) {
      setErro(err.message || 'Código OTP inválido.');
    } finally {
      setIsLoading(false);
    }
  };

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
                {/* Sempre CPF */}
                <InputField
                  label="CPF"
                  name="usuario"
                  mask="___.___.___-__"
                  value={formData.usuario}
                  onChange={handleChange}
                  icon={User}
                  disabled={precisaOTP} // bloqueia CPF no passo OTP
                />

                {/* Se não precisa OTP, mostra campo senha */}
                {!precisaOTP && (
                  <PasswordField
                    label="Senha"
                    name="senha"
                    value={formData.senha}
                    onChange={handleChange}
                  />
                )}

                {/* Se precisa OTP, mostra campo OTP */}
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

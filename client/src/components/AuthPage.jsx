import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import RegisterUser from './RegisterUser';
import FormContainer from './RegisterUser/FormContainer';
import { User, Lock } from 'lucide-react';

export default function AuthPage() {
  const [modo, setModo] = useState('login');
  const [formData, setFormData] = useState({ usuario: '', senha: '' });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setError('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.usuario || !formData.senha) {
      setError('Por favor, preencha todos os campos.');
      return;
    }
    if (formData.usuario !== 'admin' || formData.senha !== '12345678') {
      setError('Usuário ou senha incorretos.');
      return;
    }
    setError('');
    console.log('Login realizado com sucesso:', formData);
  };

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [modo]);

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className={`relative w-full ${modo === 'registro' ? 'max-w-2xl' : 'max-w-md'}`}>
        <AnimatePresence mode="wait">
          {modo === 'login' ? (
            <motion.div
              key="login"
              initial={{ opacity: 0, x: modo === 'login' ? 100 : -100 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: modo === 'login' ? -100 : 100 }}
              transition={{ duration: 0.6, ease: "easeInOut" }}

            >
              <FormContainer
                title="Acesse sua conta"
                onSubmit={handleSubmit}
                icon={<User className="text-amber-600" />}
              >
                <div>
                  <label htmlFor="usuario" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Usuário
                  </label>
                  <div className="flex items-center border border-gray-300 dark:border-gray-700 rounded-lg px-3 py-2 focus-within:ring-2 focus-within:ring-amber-600">
                    <User className="text-gray-400 mr-2" size={18} />
                    <input
                      id="usuario"
                      name="usuario"
                      type="text"
                      value={formData.usuario}
                      onChange={handleChange}
                      className="w-full bg-transparent outline-none text-gray-900 dark:text-white"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="senha" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Senha
                  </label>
                  <div className="flex items-center border border-gray-300 dark:border-gray-700 rounded-lg px-3 py-2 focus-within:ring-2 focus-within:ring-amber-600">
                    <Lock className="text-gray-400 mr-2" size={18} />
                    <input
                      id="senha"
                      name="senha"
                      type="password"
                      value={formData.senha}
                      onChange={handleChange}
                      className="w-full bg-transparent outline-none text-gray-900 dark:text-white"
                      required
                    />
                  </div>
                </div>

                <AnimatePresence>
                  {error && (
                    <motion.p
                      className="text-red-600 text-sm font-medium"
                      initial={{ opacity: 0, x: modo === 'login' ? -100 : 100 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: modo === 'login' ? 100 : -100 }}
                      transition={{ duration: 0.6, ease: "easeInOut" }}
                    >
                      {error}
                    </motion.p>
                  )}
                </AnimatePresence>

                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.96 }}
                  type="submit"
                  className="w-full bg-gradient-to-r from-amber-600 to-orange-700 hover:from-orange-700 hover:to-amber-600 text-white py-2 px-4 rounded-2xl shadow-lg transition-all duration-300 font-semibold"
                >
                  Entrar
                </motion.button>

                <p className="text-sm mt-4 text-center text-gray-600 dark:text-gray-400">
                  Não tem uma conta?{' '}
                  <button
                    onClick={() => setModo('registro')}
                    className="text-orange-700 hover:underline font-medium"
                  >
                    Cadastre-se
                  </button>
                </p>
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

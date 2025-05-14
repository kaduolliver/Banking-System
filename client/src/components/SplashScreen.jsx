import { motion } from 'framer-motion';
import { useEffect } from 'react';

export default function SplashScreen({ onComplete }) {
    useEffect(() => {
        const timer = setTimeout(() => {
            onComplete(); // Chama o fim da splash após a animação
        }, 3500); // Tempo total da splash

        return () => clearTimeout(timer);
    }, [onComplete]);
    return (       
            <motion.div
                className="fixed inset-0 flex items-center justify-center bg-black z-50"
            >
            <motion.img
                src="/images/I&L-logo.webp"
                alt="Logo"
                className="w-28 h-auto"
                initial={{ opacity: 0 }}
                animate={{ opacity: [0, 1, 0] }}
                transition={{ delay: 0.7, duration: 2.5, ease: 'easeInOut' }}
            />
            </motion.div>
        
    );
}

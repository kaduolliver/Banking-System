import { AnimatePresence, motion } from 'framer-motion';

export default function FadeBlurTransition({
  id,
  children,
  duration = 0.3,
  blur = 10,
  className = '',
}) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={id}
        initial={{ opacity: 0, filter: `blur(${blur}px)` }}
        animate={{ opacity: 1, filter: 'blur(0px)' }}
        exit={{ opacity: 0, filter: `blur(${blur}px)` }}
        transition={{ duration, ease: 'easeInOut' }}
        className={`absolute inset-0 ${className}`}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}

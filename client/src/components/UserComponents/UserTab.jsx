import * as Tabs from '@radix-ui/react-tabs';
import { motion, AnimatePresence } from 'framer-motion';

export default function UserTabs({ tabs, activeTab, setActiveTab }) {
  // Encontra o tab ativo para renderizar somente ele no AnimatePresence
  const active = tabs.find(tab => tab.value === activeTab);

  return (
    <Tabs.Root
      value={activeTab}
      onValueChange={setActiveTab}
      className="flex w-full max-w-5xl h-[500px] bg-zinc-900 rounded-xl shadow-xl overflow-hidden"
      orientation="vertical"
    >
      <Tabs.List className="flex flex-col w-52 bg-zinc-800 p-4 space-y-2">
        {tabs.map(({ value, label, icon: Icon }) => (
          <Tabs.Trigger
            key={value}
            value={value}
            className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200
              ${activeTab === value ? 'bg-orange-700 text-white' : 'text-zinc-300 hover:bg-zinc-700 hover:text-white'}`}
          >
            {Icon && <Icon className="w-5 h-5" />}
            {label}
          </Tabs.Trigger>
        ))}
      </Tabs.List>

      <div className="flex-1 p-6 relative overflow-hidden">
        <AnimatePresence mode="wait">
          {active && (
            <Tabs.Content key={active.value} value={active.value} asChild forceMount>
              <motion.div
                key={active.value}
                initial={{ opacity: 0, filter: 'blur(10px)' }}
                animate={{ opacity: 1, filter: 'blur(0px)' }}
                exit={{ opacity: 0, filter: 'blur(10px)' }}
                transition={{ duration: 0.5, ease: 'easeInOut' }}
                className="absolute inset-0"
              >
                <div className="text-white text-base">{active.content}</div>
              </motion.div>
            </Tabs.Content>
          )}
        </AnimatePresence>
      </div>
    </Tabs.Root>
  );
}

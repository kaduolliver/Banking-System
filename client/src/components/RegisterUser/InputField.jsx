import { Phone, User } from 'lucide-react';
import { InputMask } from '@react-input/mask';

export default function InputField({ label, name, value, onChange, type = 'text', mask, icon }) {
  const IconComponent = icon === 'phone' ? Phone : User;
  const inputClass = 'w-full bg-transparent outline-none text-gray-900 dark:text-white';

  return (
    <div>
      <label htmlFor={name} className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
        {label}
      </label>
      <div className="flex items-center border border-gray-300 bg-black dark:border-gray-700 rounded-lg px-3 py-2 focus-within:ring-2 focus-within:ring-amber-600">
        {icon && <IconComponent className="text-gray-400 mr-2" size={18} />}
        {mask ? (
          <InputMask
            mask={mask}
            replacement={{ _: /\d/ }}
            name={name}
            value={value}
            onChange={onChange}
            className={inputClass}
            required
          />
        ) : (
          <input
            id={name}
            name={name}
            type={type}
            value={value}
            onChange={onChange}
            className={inputClass}
            required
          />
        )}
      </div>
    </div>
  );
}
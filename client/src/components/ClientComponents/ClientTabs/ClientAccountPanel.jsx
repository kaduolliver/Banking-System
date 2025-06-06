import { useState } from 'react';
import ClientAddressForm from './ClientAddress';

export default function ClientAccountPanel() {
  const [enderecoSalvo, setEnderecoSalvo] = useState(false);

  return (
    <div>
      {!enderecoSalvo && (
        <ClientAddressForm onEnderecoSalvo={() => setEnderecoSalvo(true)} />
      )}
      {enderecoSalvo && (
        <div className="text-green-400 p-4">
          Endereço cadastrado com sucesso!
        </div>
      )}
    </div>
  );
}

import { useState } from 'react';
import ClientAddressForm from './AccountPanelComponents/ClientAddress';
import FinancialServices from './AccountPanelComponents/ClientAccountRequest';
//import ScreenOverlay from '../../EffectsComponents/ScreenOverlay';

export default function ClientAccountPanel() {
  const [enderecoSalvo, setEnderecoSalvo] = useState(false);

  return (
    <div>
      {!enderecoSalvo && (
        <ClientAddressForm onEnderecoSalvo={() => setEnderecoSalvo(true)} />
      )}

      {enderecoSalvo && (
        <>
          {/* <ScreenOverlay /> */}
          {/* <div className="text-green-400 p-4">
            Endereço cadastrado com sucesso!
          </div> */}

          <FinancialServices />
        </>
      )}
    </div>
  );
}

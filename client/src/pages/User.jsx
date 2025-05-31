import { useEffect, useState } from 'react';
import ClientTabs from '../components/ClientComponents/ClientTabs';
import EmployeeTabs from '../components/EmployeeComponents/EmployeeTabs';
import ClientNavBar from '../components/ClientComponents/ClientNavBar';
import EmpNavBar from '../components/EmployeeComponents/EmpNavBar';

export default function User() {
  const [userType, setUserType] = useState(null);

  useEffect(() => {
    const tipo = localStorage.getItem('tipo');
    if (!tipo) {
      window.location.href = '/login';
      return;
    }
    setUserType(tipo);
  }, []);

  if (!userType) return null;

  const isClient = userType === 'cliente';
  const UserNavBar = isClient ? <ClientNavBar /> : <EmpNavBar />;
  const TabsComponent = isClient ? <ClientTabs /> : <EmployeeTabs />;

  return (
    <>
      {UserNavBar}
      <div
        className="min-h-screen flex pt-40 pb-20 items-center justify-center bg-cover p-6"
        style={{ backgroundImage: "url('/images/bitcoin-bg-user.png')" }}
      >
        {TabsComponent}
      </div>
    </>
  );
}

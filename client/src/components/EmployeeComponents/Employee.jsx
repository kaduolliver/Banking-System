import { useAuth } from "../../context/authContext";
import EmployeeNavbar from "./EmpNavBar";
import EmployeeTabs from "./EmployeeTabs";
import ScreenOverlay from "../EffectsComponents/ScreenOverlay";
import SplashScreen from "../EffectsComponents/SplashScreen";

export default function Employee() {

  const { carregando } = useAuth();

  if (carregando) return <SplashScreen />;

  return (
    <>
      <ScreenOverlay />
      <EmployeeNavbar />
      <div className="min-h-screen flex pt-40 pb-20 bg-black items-center justify-center bg-cover p-6"
        style={{ backgroundImage: "url('/images/bitcoin-bg-user.png')" }}>
        <EmployeeTabs />
      </div>
    </>
  );
}

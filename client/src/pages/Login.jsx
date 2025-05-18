import ScreenOverlay from "../components/ScreenOverlay";
import AuthPage from "../components/LoginUser";

export default function LoginUser() {
  return (
    <>
      <ScreenOverlay />
      <div
        className="pt-20 bg-cover bg-center bg-fixed bg-black animate-fade-in delay-[500ms] min-h-screen"
        style={{ backgroundImage: "url('/images/bg-login.jpg')" }}>
        <div className="max-w-lg mx-auto flex flex-col justify-center px-4">
          <AuthPage />
        </div>
      </div>
    </>
  );
}
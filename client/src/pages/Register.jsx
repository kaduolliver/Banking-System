import ScreenOverlay from "../components/ScreenOverlay";
import RegisterUser from "../components/RegisterUser";

export default function Register() {
    return (
        <>
            <ScreenOverlay />
            <div
                className="pt-20 bg-cover bg-center bg-fixed bg-black animate-fade-in delay-[500ms]"
                style={{ backgroundImage: "url('/images/bg-register.jpg')" }}
            >
                <div className="max-w-2xl mx-auto px-4 py-12 pb-40">
                    {/* pb-40 cria espaço extra para o Footer */}
                    <RegisterUser />
                </div>
            </div>
        </>
    );
}

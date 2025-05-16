import ScreenOverlay from "../components/ScreenOverlay";

export default function Home() {
    return (
        <>
            <ScreenOverlay />
            <div
                className="pt-20 min-h-screen bg-cover bg-center bg-black flex items-center justify-center animate-fade-in delay-[500ms]"
                style={{ backgroundImage: "url('/images/bg-img.jpg')" }}>
                <div class="relative right-80 animate-fade-in-up">
                    <img src="/images/I&L-logo.webp" alt="logo" className="w-56 h-auto"></img>
                    <h1 className="text-8xl text-white font-bold text-left pb-6" style={{ fontFamily: 'Bodoni FLF' }}>Infinity & <br />Legacy Group</h1>
                    <h1 className="text-xl text-[#9b9b9b] font-bold text-left typing-effect" style={{ fontFamily: 'Aileron, sans-serif' }}>"Investindo no amanhã, honrando o ontem."</h1>
                </div>
            </div>
        </>
    )
}
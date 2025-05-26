import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import ScreenOverlay from "../components/EffectsComponents/ScreenOverlay";
import InitialsBar from "../components/EffectsComponents/InitialsBar";
import Navbar from "../components/navbar";

const images = [
    "/images/luxury-bg-about.jpg",
    "/images/about-bg.jpg",
    "/images/meet-bg-about.jpg",
    "/images/handshake-bg-about.jpg",
    "/images/exchange-bg-about.jpg"
];

export default function About() {
    const [currentIndex, setCurrentIndex] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentIndex((prev) => (prev + 1) % images.length);
        }, 6000);
        return () => clearInterval(interval);
    }, []);

    return (
        <>
            <ScreenOverlay />
            <Navbar />
            <div className="relative pt-20 min-h-screen overflow-hidden">
                <AnimatePresence mode="wait">
                    <motion.div
                        key={images[currentIndex]}
                        initial={{ opacity: 0, scale: 1.05 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.98 }}
                        transition={{ duration: 1, ease: [0.42, 0, 0.58, 1] }}
                        className="absolute inset-0 bg-cover bg-center"
                        style={{ backgroundImage: `url(${images[currentIndex]})` }} />
                </AnimatePresence>

                <div className="relative z-10 flex min-h-screen">
                    <div className="w-3/4 bg-gradient-to-r from-black via-gray-900 to-transparent flex flex-col justify-center pl-16">
                        <motion.div
                            className="relative bottom-10"
                            initial={{ x: -100, opacity: 0 }}
                            animate={{ x: 0, opacity: 1 }}
                            transition={{ duration: 1, delay: 0.3, ease: [0.42, 0, 0.58, 1] }}>
                            <h1 className="text-6xl lg:text-8xl bg-gradient-to-r from-amber-600 to-orange-700 text-transparent bg-clip-text font-extrabold text-left">Bem-vindo a</h1>
                            <h1 className="text-6xl lg:text-8xl text-white font-bold text-left pb-5" style={{ fontFamily: "Bodoni FLF" }}>Infinity & <br /> Legacy Group</h1>
                            <div className="relative space-y-2">
                                {/* Linha 1 */}
                                <div className="relative inline-block">
                                    <motion.div
                                        initial={{ scaleX: 0 }}
                                        animate={{ scaleX: 1 }}
                                        transition={{ duration: 1, delay: 0.8, ease: [0.42, 0, 0.58, 1] }}
                                        className="absolute inset-0 bg-white rounded shadow-sm origin-left z-0"
                                    />
                                    <span className="relative z-10 text-xl text-black p-1 inline-block">
                                        Com uma trajetória marcada por inovação, transparência e excelência no
                                    </span>
                                </div>

                                {/* Linha 2 */}
                                <div className="relative inline-block">
                                    <motion.div
                                        initial={{ scaleX: 0 }}
                                        animate={{ scaleX: 1 }}
                                        transition={{ duration: 1, delay: 1, ease: [0.42, 0, 0.58, 1] }}
                                        className="absolute inset-0 bg-white rounded shadow-sm origin-left z-0"
                                    />
                                    <span className="relative z-10 text-xl text-black p-1 inline-block">
                                        atendimento, nossa missão é facilitar o acesso a serviços bancários de qualidade,
                                    </span>
                                </div>

                                <div className="relative inline-block">
                                    <motion.div
                                        initial={{ scaleX: 0 }}
                                        animate={{ scaleX: 1 }}
                                        transition={{ duration: 1, delay: 1.2, ease: [0.42, 0, 0.58, 1] }}
                                        className="absolute inset-0 bg-white rounded shadow-sm origin-left z-0"
                                    />
                                    <span className="relative z-10 text-xl text-black p-1 inline-block">
                                        ajudando pessoas e empresas a alcançarem seus objetivos financeiros.
                                    </span>
                                </div>
                            </div>

                        </motion.div>
                    </div>
                    <div className="w-1/2" />
                </div>
            </div>
            <InitialsBar />
            <div
                className="pt-20 bg-cover bg-center bg-black animate-fade-in delay-[500ms] min-h-screen"
                style={{ backgroundImage: "url('/images/bg-about-2.jpg')" }}>
            </div>

        </>
    );
}
import './App.css';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Market from './pages/Market';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import { AnimatePresence } from "framer-motion";
import { useState } from 'react';
import SplashScreen from './components/SplashScreen';

export default function App() {
  const [showSplash, setShowSplash] = useState(true);
  return (
    <>
      <AnimatePresence>
        {showSplash && <SplashScreen onComplete={() => setShowSplash(false)} />}
      </AnimatePresence>

      {!showSplash && (
        <>
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/market" element={<Market />} />
          </Routes>
          <Footer />
        </>
      )}
    </>
  );
}
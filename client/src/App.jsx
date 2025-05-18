import './App.css';
import { Routes, Route, useLocation } from 'react-router-dom';
import Home from './pages/Home';
import Market from './pages/Market';
import Login from './pages/Login';
import About from './pages/About';
import User from './pages/User';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import { AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import SplashScreen from './components/SplashScreen';

export default function App() {
  const [showSplash, setShowSplash] = useState(true);
  const location = useLocation();

  const ocultarFooter = [''];

  return (
    <>
      <AnimatePresence>
        {showSplash && <SplashScreen onComplete={() => setShowSplash(false)} />}
      </AnimatePresence>

      {!showSplash && (
        // Main Container
        <div className="main-container">
          {/* Header */}
          <header className="header-content">
            <Navbar />
          </header>

          {/* Content */}
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/market" element={<Market />} />
              <Route path="/login" element={<Login />} />
              <Route path="/about" element={<About />} />
              <Route path="/user" element={<User />} />
            </Routes>
          </main>

          {/* Footer */}
          {!ocultarFooter.includes(location.pathname) && (
            <footer className="footer-content">
              <Footer />
            </footer>
          )}
        </div>
      )}
    </>
  );
}

import './App.css'
import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Market from './pages/Market'
import Navbar from './components/Navbar'
import Footer from './components/Footer'

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/market" element={<Market />} />
      </Routes>
      <Footer />
    </>
  );
}

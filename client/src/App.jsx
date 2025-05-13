import './App.css'
import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Market from './pages/Market'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/market" element={<Market />} />
    </Routes>
  );
}

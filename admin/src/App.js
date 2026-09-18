import { Routes, Route } from 'react-router-dom'; 
import './App.css';
import Home from './Components/Home';
import Login from './Components/Login';
import Logout from './Components/Logout';
import Register from './Components/Register';
import Navbar from './Components/Navbar';


function App() {
  return (
    <div>
      <Navbar></Navbar>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/logout" element={<Logout />} />
      </Routes>
    </div>
  );
}

export default App;

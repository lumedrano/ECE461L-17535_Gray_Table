import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Login from './pages/Login';
import Home from './pages/Home';
import { AuthProvider } from './components/logincomponents/Auth';
import PrivateRoute from './components/logincomponents/PrivateRoute';
import Hardware from './pages/Hardware';  // Adjust path if needed

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Login/>}></Route>
          <Route path="/login" element={<Login/>}></Route>
          <Route element={<PrivateRoute />}>
            <Route path="/projects" element={<Home />} />
            <Route path="/hardware" element={<Hardware />} /> 
          </Route>
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;

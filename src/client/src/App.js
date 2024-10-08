import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Login from './pages/Login';
import Home from './pages/Home';

function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Login/>}></Route>
          <Route path="/login" element={<Login/>}></Route>
          <Route path="/projects" element={<Home/>}></Route>
        </Routes>
      </Router>
    </div>
  );
}

export default App;

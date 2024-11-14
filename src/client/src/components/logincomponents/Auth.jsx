import React, { createContext, useState, useContext, useEffect } from 'react';
import { useCookies } from 'react-cookie';

const Auth = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [cookies] = useCookies(['userID']);

  useEffect(() => {
    if (cookies.userID) {
      setIsAuthenticated(true);
    }
  }, [cookies.userID]);

  const login = (userId) => {
    setIsAuthenticated(true);
  };

  const logout = () => {
    setIsAuthenticated(false);
  };

  return (
    <Auth.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </Auth.Provider>
  );
};

export const useAuth = () => useContext(Auth);
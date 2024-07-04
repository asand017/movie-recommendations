'use client';

import React, { createContext, useState, useEffect, useContext } from 'react';
import { useRouter } from 'next/navigation';
import { jwtDecode } from 'jwt-decode';

// Define the shape of the AuthContext state
interface AuthContextState {
  isAuthenticated: boolean;
  user: string | null;
  login: (token: string) => void;
  logout: () => void;
}

// Create the AuthContext with default values
const AuthContext = createContext<AuthContextState>({
  isAuthenticated: false,
  user: null,
  login: () => {},
  logout: () => {},
});

// Define a helper function to check if a JWT is expired
const isTokenExpired = (token: string) => {
  const decodedToken: any = jwtDecode(token);
  return decodedToken.exp * 1000 < Date.now();
};

// Create the AuthProvider component
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token && !isTokenExpired(token)) {
      setIsAuthenticated(true);
      setUser(jwtDecode(token).sub || null); // Assuming the username is in the "sub" claim
    } else {
      localStorage.removeItem('auth_token');
      setIsAuthenticated(false);
      setUser(null);
    }
  }, []);

  const login = (token: string) => {
    console.log('logging in with token: ', token);
    localStorage.setItem('auth_token', token);
    setIsAuthenticated(true);
    setUser(jwtDecode(token).sub || null);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the AuthContext
export const useAuth = () => useContext(AuthContext);
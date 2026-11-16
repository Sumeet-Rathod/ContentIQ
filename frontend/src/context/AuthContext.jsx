import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [tenant, setTenant] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('contentiq_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initializeAuth = async () => {
      const storedToken = localStorage.getItem('contentiq_token');
      if (storedToken) {
        try {
          const res = await authApi.getMe();
          setUser(res.data.user);
          setTenant(res.data.tenant);
        } catch (err) {
          console.error('Session restoration failed:', err);
          logout();
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (email, password) => {
    const res = await authApi.login({ email, password });
    const { access_token, user: userData, tenant: tenantData } = res.data;
    localStorage.setItem('contentiq_token', access_token);
    localStorage.setItem('contentiq_user', JSON.stringify(userData));
    if (tenantData) {
      localStorage.setItem('contentiq_tenant', JSON.stringify(tenantData));
      setTenant(tenantData);
    }
    setToken(access_token);
    setUser(userData);
    return res.data;
  };

  const register = async (payload) => {
    const res = await authApi.register(payload);
    const { access_token, user: userData, tenant: tenantData } = res.data;
    localStorage.setItem('contentiq_token', access_token);
    localStorage.setItem('contentiq_user', JSON.stringify(userData));
    if (tenantData) {
      localStorage.setItem('contentiq_tenant', JSON.stringify(tenantData));
      setTenant(tenantData);
    }
    setToken(access_token);
    setUser(userData);
    return res.data;
  };

  const logout = () => {
    localStorage.removeItem('contentiq_token');
    localStorage.removeItem('contentiq_user');
    localStorage.removeItem('contentiq_tenant');
    setToken(null);
    setUser(null);
    setTenant(null);
  };

  const value = {
    user,
    tenant,
    token,
    loading,
    login,
    register,
    logout,
    isAdmin: user?.role === 'admin',
    isEditor: user?.role === 'editor',
    isClient: user?.role === 'client',
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

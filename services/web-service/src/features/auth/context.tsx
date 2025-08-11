"use client";

import { createContext, useState, ReactNode, useEffect } from "react";
import { User } from "./types";
import { login as loginService } from "./service";
import { getStoredToken, setStoredToken, removeStoredToken } from "@/lib/auth";

type AuthContextType = {
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
};

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const token = getStoredToken();
    if (token) {
      // Optional: decode JWT to retrieve user
      const decoded = JSON.parse(atob(token.split(".")[1]));
      setUser({username: decoded.sub});
    }
  }, []);

  async function login(username: string, password: string) {
    const res = await loginService(username, password); //const { user, token } = 
    setUser(user);
    setStoredToken(token);
  }

  function logout() {
    setUser(null);
    removeStoredToken();
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
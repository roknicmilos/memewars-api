import { createContext, useContext, ReactNode, useState } from "react";
import { User } from "../models/user";
import { authService } from "../services/authService";

interface AuthContextValues {
  user: User | null;

  saveUser(user: User): void;

  clearUser(): void;
}

const AuthContext = createContext<AuthContextValues>({
  user: null,
  saveUser: () => {
    throw new Error("Not implemented");
  },
  clearUser: () => {
    throw new Error("Not implemented");
  },
});

export function AuthContextProvider({ children }: { children: ReactNode }) {
  const [ user, setUser ] = useState<User | null>(authService.getUserFromLocalStorage);

  function saveUser(user: User): void {
    localStorage.setItem("user", JSON.stringify(user));
    setUser(user);
  }

  function clearUser(): void {
    localStorage.removeItem("user");
    setUser(null);
  }

  return (
    <AuthContext.Provider value={ { user, saveUser, clearUser } }>
      { children }
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

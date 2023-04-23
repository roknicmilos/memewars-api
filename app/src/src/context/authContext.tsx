import { createContext, ReactNode, useContext, useState } from "react";
import { User } from "../models/User";
import { authService } from "../services/authService";
import { localStorageService } from "../services/localStorageService";

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
  const [ user, setUser ] = useState<User | null>(localStorageService.getUser);

  function saveUser(user: User): void {
    localStorageService.saveUser(user);
    setUser(user);
  }

  async function clearUser(): Promise<void> {
    authService.logout();
    localStorageService.deleteUser();
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

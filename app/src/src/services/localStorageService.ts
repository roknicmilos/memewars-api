import { User } from "../models/User";

export const localStorageService = {

  saveUser(user: User): void {
    localStorage.setItem("user", JSON.stringify(user));
  },

  getUser(): User {
    const jsonUser = localStorage.getItem("user");
    return jsonUser ? JSON.parse(jsonUser) : null;
  },

  deleteUser(): void {
    localStorage.removeItem("user");
  },

};

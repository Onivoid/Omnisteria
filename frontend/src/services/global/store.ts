import { create } from "zustand";

type AuthenticatedUser = {
  token: string|undefined;
  name: string|undefined;
  isAdmin: boolean|undefined;
};

type State = {
  user: AuthenticatedUser | undefined;
  setUser: (user: AuthenticatedUser) => void;
};

export const useStore = create<State>((set) => ({
  user: undefined,
  setUser: (user: AuthenticatedUser) => set({ user }),
}));
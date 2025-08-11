// src/features/auth/types.ts

export type User = {
  username: string;
  email?: string;
};

export type AuthResponse = {
  user: User;
  token: string;
};


export type FormData = {
    username: string;
    password: string;
}
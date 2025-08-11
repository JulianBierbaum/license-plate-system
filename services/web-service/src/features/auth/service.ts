import { api_auth } from "@/lib/api";

export async function login(username: string, password: string) {
    try {
        const formData = new FormData();
        formData.append("grant_type", "password");
        formData.append('username', username); // FastAPI OAuth2PasswordRequestForm uses 'username'
        formData.append('password', password);
        console.log(formData);
        const response = await fetch("http://localhost:8000/auth/v1/login/", { //`${api_auth}`
            method: 'POST',
            body: formData,
        });
        // const response = await api_auth.post<FormData>("/login");
        console.log(response);
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
    console.log("✅ Login erfolgreich:");
    return true;
  };

//     const { data } = await api_auth.post<FormData>("/login", { username, password });
//     return data;
// }


// export async function login(username: string, password: string): Promise<AuthResponse> {
//   const { data } = await api_auth.post<AuthResponse>("/login", { username, password });
//   return data;
// }
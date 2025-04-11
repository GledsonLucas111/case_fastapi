"use client";

import { UserService } from "@/services/userService";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Alert, Box, Button, TextField } from "@mui/material";

export default function Login() {
  const userService = new UserService();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { push } = useRouter();
  const [error, setError] = useState(null);

  const submit = (e: React.FormEvent) => {
    userService
      .login({ email, password })
      .then((response) => {
        localStorage.setItem("dataUser", JSON.stringify(response.data));
        push("/home");
      })
      .catch((error) => {
        setError(error.response.data.detail || "Erro");
        setTimeout(() => {
          setError(null);
        }, 5000);
      });
    e.preventDefault();
  };

  const handleInputChange =
    (setter: React.Dispatch<React.SetStateAction<string>>) =>
    (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
      setter(e.target.value);
    };

  return (
    <div className="flex flex-col justify-center items-center h-full gap-5 pt-5">
      {error && (
        <Alert variant="filled" severity="error">
          {error}
        </Alert>
      )}
      <h3 className="text-4xl">Login</h3>
      <Box
        component="form"
        onSubmit={submit}
        className="flex flex-col gap-5 w-85"
      >
        <TextField
          label="Email"
          variant="outlined"
          type="email"
          onChange={handleInputChange(setEmail)}
          required
        />
        <TextField
          label="Senha"
          variant="outlined"
          type="password"
          onChange={handleInputChange(setPassword)}
          required
        />
        <Button variant="contained" type="submit">
          {" "}
          Entrar
        </Button>
      </Box>
    </div>
  );
}

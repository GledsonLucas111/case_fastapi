"use client";

import { UserService } from "@/services/userService";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Box, Button, TextField } from "@mui/material";

export default function Login() {
  const userService = new UserService();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { push } = useRouter();

  const submit = (e: React.FormEvent) => {
    userService
      .login({ email, password })
      .then((response) => {
        localStorage.setItem("dataUser", JSON.stringify(response.data));
        push("/home");
      })
      .catch((error) => alert(error));
    e.preventDefault();
  };

  const handleInputChange =
    (setter: React.Dispatch<React.SetStateAction<string>>) =>
    (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
      setter(e.target.value);
    };

  return (
    <div className="flex flex-col justify-center items-center h-full gap-5">
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
        <Button variant="contained" type="submit"> Entrar</Button>
      </Box>

      <p className="font-bold mt-10">
        Você não possui uma conta?{" "}
        <Button href={"/signup"} size="small">
          cadastre-se
        </Button>
      </p>
    </div>
  );
}

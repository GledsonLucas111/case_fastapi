"use client";

import { CardCourse } from "@/components/cardCourse";
import FormDialog from "@/components/formDialog";
import Header from "@/components/header";
import { Box, Button, Typography } from "@mui/material";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function Home() {
  const { push } = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("dataUser")
  );

  useEffect(() => {
    if (!isLoggedIn) {
      push("/");
    }
  }, [isLoggedIn, push]);

  if (!isLoggedIn) {
    return null;
  }

  function getUserData() {
    const dados = localStorage.getItem("dataUser");
    if (dados) {
      const user = JSON.parse(dados);
      return user;
    } else {
      console.log("Nenhum usuário encontrado no localStorage.");
    }
  }

  return (
    <div className="">
      <Header user={getUserData()} />
      {getUserData().role === "teacher" ? (
        <Box className="flex items-center p-5 gap-10">
          <Typography variant="subtitle1" className="">
            Meus cursos:
          </Typography>
          <FormDialog id={getUserData().id} />
        </Box>
      ) : (
        <Box className="flex items-center p-5 gap-10">
          <Typography variant="subtitle1" className="">
            Cursos matriculados
          </Typography>
          <Button className="h-7" variant="contained" onClick={()=> push("/courses")}>Procurar novos cursos</Button>
        </Box>
      )}
      <CardCourse user={getUserData()} />
    </div>
  );
}

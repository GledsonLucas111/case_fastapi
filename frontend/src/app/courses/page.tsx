"use client";

import { CardCourse } from "@/components/cardCourse";
import Header from "@/components/header";
import { UserService } from "@/services/userService";
import { Box, Typography } from "@mui/material";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function Courses() {
  const { push } = useRouter();
  const userService = new UserService();
  const [dataUser, setDataUser] = useState([]);
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("dataUser")
  );

  useEffect(() => {
    if (!isLoggedIn) {
      push("/");
    }
    userService
      .list()
      .then((response) => {
        const new_users = response.data.filter(
          (user: any) => user.role === "teacher"
        );
        setDataUser(new_users);
      })
      .catch((error) => console.log(error));
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
    <Box>
      <Header user={getUserData()} />
      {dataUser.map((user: any)=> {
        return(
            <Box  key={user.id}>
                <Typography className="p-5" fontWeight={600}>Professor: {user.name}</Typography>
                <CardCourse user={user}/>
            </Box>
        )
      })}
    </Box>
  );
}

"use client";

import { useState } from "react";

export default function Home() {

  function getUserData() {
    const dados = localStorage.getItem("dataUser");
    if (dados) {
      const user = JSON.parse(dados);
      return user;
    } else {
      console.log("Nenhum usuário encontrado no localStorage.");
    }
  }

  console.log(getUserData());
  return (
    <div className="">
      <header className="p-10 bg-blue-900">la</header>
      {getUserData().role === "teacher"? <h1>Meus cursos</h1>: <h1>Cursos</h1>}
    </div>
  );
}

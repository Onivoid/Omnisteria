import Head from "next/head";
import { Inter } from "next/font/google";
import styles from "@/styles/pages/Admin.module.scss";
import { InputText } from "primereact/inputtext";
import { Button } from "primereact/button";
import { useState } from "react";
import { login } from "@/services/Auth/functions/login";
import { Notifications } from "@/components/notifications";

const inter = Inter({ subsets: ["latin"] });

export default function Admin() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [type, setType] = useState("");

  const handleLogin = async () => {
    if(email === "" || password === "") {
      setMessage("Veuillez remplir tous les champs");
      setType("warning");
      return;
    }
    const result = await login(email, password);
    console.log(result);
    if(result.status !== 200) {
      setMessage("Compte introuvable");
      setType("error");
      return;
    };
    if(!result.data.isAdmin) {
      setMessage("Ce compte ne possède pas les droits d'administrateur");
      setType("warning");
    } else {
      setMessage("Connexion réussie");
      setType("success");
    }
  };

  return (
    <>
      <Head>
        <title>Login</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className={`${styles.main} ${inter.className}`}>
        <Notifications message={message} type={type} />
        <div className={styles.formContainer}>
          <InputText placeholder="Email" onChange={(e) => setEmail(e.target.value)}/>
          <InputText placeholder="Password" type="password" onChange={(e) => setPassword(e.target.value)}/>
          <Button label="Login" onClick={handleLogin}/>
        </div>
      </main>
    </>
  );
}

import Login from "@/components/admin/login";
import Panel from "@/components/admin/panel";
import { useStore } from "@/services/global/store";
import { useState } from "react";
import { login } from "@/services/auth/login";
import { Notifications } from "@/components/notifications";
import Style from "@/styles/pages/Admin.module.scss";

export default function Admin() {
  const user = useStore(state => state.user);
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [notifications, setNotifications] = useState<{message: string, type: string}[]>([]);

  const handleLogin = async () => {
    if(name === "" || password === "") {
      setNotifications([{ message: "Veuillez remplir tous les champs", type: "warning" }]);
      return;
    }

    const result = await login(name, password);

    if (result.typename === "Error"){
      if (result.message) setNotifications([{ message: result.message, type: "error" }]);
      return;
    } 

    if(!result.isAdmin){
      setNotifications([{ message: "Vous n'êtes pas administrateur.", type: "error" }]);
      return;
    }else {
      useStore.setState({user: {name: result.name, token: result.token, isAdmin: result.isAdmin}});
      setNotifications([{ message: "Vous êtes connecté", type: "success" }]);
      return;
    }
  };
  return (
    <>
    <Notifications notifications={notifications} />
      {
        user && user.isAdmin
          ? <Panel token={user.token!}/> 
          : <Login setName={setName} setPassword={setPassword} handleLogin={handleLogin} />}
    </>
  );
}

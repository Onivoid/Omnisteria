import { useQuery } from "@apollo/client";
import { GET_ALL_USERS } from "@/services/graphql/UsersQuery";
import { useState, useEffect } from "react";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import styles from "@/styles/components/Panel.module.scss"
import UserActions from "@/components/admin/userActions";

export default function Panel({ token }: { token: string }) {
  const [users, setUsers] = useState([]);

  const { data } = useQuery(GET_ALL_USERS, {
    context: {
      headers: {
        Authorization: token,
      },
    },
  });
  useEffect(() => {
    if (data) {
      setUsers(data.users.users);
    }
  }, [data]);
  return (
    <main className={`${styles.main}`}>
      <h1>Admin Panel</h1>
      <div className={styles.container}>
        <DataTable value={users} paginator rows={5} rowsPerPageOptions={[5, 10, 25, 50]}>
          <Column field="id" header="ID" style={{ width: "25%" }}></Column>
          <Column field="name" header="Name" style={{ width: "5%" }}></Column>
          <Column body={(rowData) => rowData.characters.length} field="characters" header="Characters" style={{ width: "5%" }}></Column>
          <Column header="Actions" style={{ width: "65%" }} body={(rowData => <UserActions userID={rowData.id}/>)}></Column>
        </DataTable>
      </div>
    </main>
  );
}

import Head from "next/head";
import { Inter } from "next/font/google";
import styles from "@/styles/pages/admin/User.module.scss";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { useQuery } from "@apollo/client";
import { GET_USER_BY_ID } from "@/services/graphql/UsersQuery";
import { useStore } from "@/services/global/store";
import { User as UserType} from "@/services/types/User";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import Link from "next/link";
import CharacterActions from "@/components/admin/characterActions";

const inter = Inter({ subsets: ["latin"] });

export default function User() {
  const admin = useStore(state => state.user);
  const token = admin?.token;
  const [user, setUser] = useState<UserType | undefined>(undefined);
  const router = useRouter();
  const userID: string = router.query.id as string;

  const { data, refetch, loading } = useQuery(GET_USER_BY_ID, {
    context: {
      headers: {
        Authorization: token,
        user_id: userID,
      },
      skip: !userID,
      fetchPolicy: "network-only",
    },
  });

  useEffect(() => {
    if (userID) {
      refetch();
    }
  }, [userID, refetch]);

  useEffect(() => {
    if (data) {
      setUser(data.user);
    }
  }, [data]);

  return (
    <>
      <Head>
        <title>USER</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className={`${styles.main} ${inter.className}`}>
        <Link href="/admin">Back</Link>
        <h1>User : {loading ? "Chargement ..." : user?.name}</h1>
        <h2>ID : {loading ? "Chargement ..." : user?.id}</h2>
        <div className={styles.container}>
          <DataTable value={loading ? undefined : user?.characters} paginator rows={5} rowsPerPageOptions={[5, 10, 25, 50]}>
            <Column field="id" header="ID" style={{ width: "20%" }}></Column>
            <Column field="name" header="Name" style={{ width: "20%" }}></Column>
            <Column field="type.name" header="Type" style={{ width: "20%" }}></Column>
            <Column field="level" header="Level" style={{ width: "20%" }}></Column>
            <Column body={(rowData => <CharacterActions characterID={rowData.id}/>)} header="Actions" style={{ width: "20%" }}></Column>
          </DataTable>
        </div>
      </main>
    </>
  );
}
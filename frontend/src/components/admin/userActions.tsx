import Link from "next/link"
import styles from "@/styles/components/UserActions.module.scss" 

export default function UserActions({ userID }: { userID: string }) {
  return (
    <div className={styles.container}>
      <Link href={`/admin/user/${userID}`} className={styles.infoButton}> Infos </Link>
      <Link href={`/admin/`} className={styles.deleteButton}> Delete </Link>
    </div>
  )
}
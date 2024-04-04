import { useQuery } from '@apollo/client';
import { GET_ALL_USERS } from '@/services/graphql/UsersQuery';

export default function Panel({token}:{token: string} ){
    const {data} = useQuery(GET_ALL_USERS, {
      context: {
        headers: {
          "Authorization": token
        }
      }
    });

    console.log(data);
    return (
        <h1>Admin Panel</h1>
    )
}
import dotenv from 'dotenv';
import axios from 'axios';

dotenv.config();

const login = async (email: string, password: string) => {
  try {
    const response = await axios.post(`${process.env.NEXT_PUBLIC_BACKEND_URL}/users/login`, {
      email,
      password
    });

    console.log(response);
    return response.data;
  } catch (error) {
    return error;
  }
};

export { login };
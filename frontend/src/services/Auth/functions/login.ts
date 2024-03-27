import dotenv from 'dotenv';
import axios, { AxiosResponse } from 'axios';

dotenv.config();

const login = async (email: string, password: string) : Promise<AxiosResponse> =>{
  try {
    const response = await axios.post(`${process.env.NEXT_PUBLIC_BACKEND_URL}/users/login`, {
      email,
      password
    });
    return response;
  } catch (error) {
    return error as AxiosResponse<any, any>;
  }
};

export { login };
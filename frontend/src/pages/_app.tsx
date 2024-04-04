import "@/styles/global/index.scss";
import 'primereact/resources/themes/lara-dark-indigo/theme.css';
import 'primeicons/primeicons.css';
import 'primereact/resources/primereact.css';
import 'primeflex/primeflex.css';  
import type { AppProps } from "next/app";
import { PrimeReactProvider } from "primereact/api";
import { ApolloProvider, ApolloClient, InMemoryCache } from "@apollo/client";
import dotenv from 'dotenv';
import { useStore } from "@/services/global/store";

dotenv.config();

export const client = new ApolloClient({
  uri: process.env.NEXT_PUBLIC_BACKEND_URL,
  cache: new InMemoryCache(),
});

export default function App({ Component, pageProps }: AppProps) {
  useStore.subscribe(({user}) => {
    console.log(user);
  });
  return (
    <ApolloProvider client={client}>
      <PrimeReactProvider>
        <Component {...pageProps} />
      </PrimeReactProvider>
    </ApolloProvider>
  );
}

import type { AppProps } from 'next/app';
import { ModalAuth } from '../components/Modals/ModalAuth';
import { wrapper } from '../redux/store';
import '../styles/globals.scss';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useRouter } from 'next/router';
import React from 'react';
import { Alert } from '../components/Alert';
import { ModalWrapper } from '../contexts/modals';
import { AlertWrapper } from '../contexts/alert';



function MyApp({Component, pageProps: {session, ...pageProps}}: AppProps) {
  const router = useRouter();
  return (
    <>
      <ModalWrapper>
        <AlertWrapper>
          <Component {...pageProps} />
          <ModalAuth isMainPage={router.pathname == '/'}/>
          <Alert />
        </AlertWrapper>
      </ModalWrapper>
    </>
  )
}



export default wrapper.withRedux(MyApp);


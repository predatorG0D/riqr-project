import { createContext, Dispatch, SetStateAction, useContext, useState } from 'react';

const initialState = {
    isShow: false,
    name: '',
    pageIdDelete: undefined
}

const ModalContext = createContext<ModalContext >({} as ModalContext);

interface ModalState {
    isShow: boolean,
    name: string,
    tabId?: string;
    pageIdDelete?: number
}
interface ModalContext {
    state: ModalState,
    setModal: Dispatch<SetStateAction<ModalState>>
}


export function ModalWrapper({ children }: any) {
    const [state, setModal] = useState<ModalState>(initialState);

  return (
    <ModalContext.Provider value={{state, setModal}}>
      {children}
    </ModalContext.Provider>
  );
}

export function useModalContext() {
  return useContext(ModalContext);
}
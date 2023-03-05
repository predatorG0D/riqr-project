import { createContext, Dispatch, SetStateAction, useContext, useState } from 'react';

const initialState = {
    isShow: false,
    isSuccess: false,
    text: '',
}

const AlertContext = createContext<AlertContext >({} as AlertContext);

export interface AlertState {
    isShow: boolean,
    isSuccess: boolean
    text: string,
}
export interface AlertContext {
    state: AlertState,
    setState: Dispatch<SetStateAction<AlertState>>
}


export function AlertWrapper({ children }: any) {
    const [state, setState] = useState<AlertState>(initialState);

    return (
        <AlertContext.Provider value={{state, setState}}>
        {children}
        </AlertContext.Provider>
    );
}

export function useAlertContext() {
  return useContext(AlertContext);
}
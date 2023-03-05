import { getCookie } from './../../utils/cookies';
import router from "next/router";
import { Dispatch } from "redux";
import { entryGoogleReq, entryVkReq, loginReq, logoutReq, registerReq, verifyEmailReq } from "../../api/auth";
import { AlertContext } from "../../contexts/alert";
import authContants from "../constants/auth";


export const authenticateAction = (data: any) => {
   return {
       type: authContants.AUTHENTICATE,
       payload: data
   };
};


export const deAuthenticateAction = () => {
   return {
       type: authContants.DEAUTHENTICATE,
   };
};

export const vkAction = (user:any) => {
    return {
        type: authContants.AUTHENTICATE_VK,
        payload: user
    };
};

export const googleAction = (user: any) => {
    return {
        type: authContants.AUTHENTICATE_GOOGLE,
    };
};

export const restoreState = (authState: any) => {
   return {
       type: authContants.RESTORE_AUTH_STATE,
       payload: authState
   }
};

export const entryVk = (code: any) => {
    return (dispatch: Dispatch, getState: any) => {
        const { isLoggedIn} = getState().auth;
        entryVkReq(code).then((res: any)=>{
            dispatch(deAuthenticateAction());
            dispatch(authenticateAction(res.data));

            router.push('/cabinet');
        }).catch(()=> {
            if(isLoggedIn) {
                router.push('/cabinet');
                
            }else {
                dispatch(deAuthenticateAction());
                router.push('/');
            }
        })
    }
}


export const entryGoogle = (code: any) => {
    
    return (dispatch: Dispatch, getState: any) => {
        const { isLoggedIn} = getState().auth;
        entryGoogleReq(code).then((res: any)=>{
            dispatch(deAuthenticateAction());
            dispatch(authenticateAction(res.data));

            router.push('/cabinet');
        }).catch(()=> {
            if(isLoggedIn) {

                router.push('/cabinet');
            }else {
                dispatch(deAuthenticateAction());
                router.push('/');
            }
            
        })
    }
}

export const login = (data: any, alert: AlertContext) => {
    return (dispatch: Dispatch) => {
        dispatch(deAuthenticateAction());
        loginReq({user: data}).then((res: any)=>{
            
            dispatch(authenticateAction(res.data));
            alert.setState({isShow: true, isSuccess: true, text: 'Вы успешно вошли в аккаунт'});
            router.push('/cabinet');
        }).catch(()=> {
            alert.setState({isShow: true, isSuccess: false, text: 'Не получилось войти в аккаунт'})
            router.push('/');
        })
    }
};


export const register = (data: any, alert: AlertContext) => (dispatch: Dispatch) => {
    registerReq({user: data}).then((res: any) => {
        alert.setState({isShow: true, isSuccess: true, text: 'Подтведите e-mail на почте для завершения регистрации'})
        dispatch(deAuthenticateAction());
    }).catch(()=> {
        alert.setState({isShow: true, isSuccess: false, text: 'Не получилось зарегистрироваться'});
        dispatch(deAuthenticateAction());
        
        router.push('/');
    })
}

export const verifyEmail = (hash: any) => (dispatch: Dispatch) => {
    verifyEmailReq(hash).then((res: any) => {
        dispatch(deAuthenticateAction());
        dispatch(authenticateAction(res.data));
        router.push('/cabinet');
    }).catch(()=> {
        // alert.setState({isShow: true, isSuccess: false, text: 'Не получилось зарегистрироваться'});
        dispatch(deAuthenticateAction());
        
        router.push('/');
    })
}


export const logout = () => {
    return async (dispatch: Dispatch, getState: any) => {
        const refresh = getCookie("refresh");

        if (refresh) {
            await logoutReq(refresh);
        }
        
        dispatch(deAuthenticateAction());
        router.push('/');
    }
};


export const restore = (savedState: any) => {
   return (dispatch: Dispatch) => {
       dispatch(restoreState(savedState));
   };
};

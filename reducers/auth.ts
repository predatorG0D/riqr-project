import { AnyAction } from "redux";
import { getCookie, remCookie, setCookie } from "../../utils/cookies";
import authConst from '../constants/auth';

let initialState = {};
if (typeof localStorage !== "undefined") {
   const authToken = getCookie('access');
   const refreshToken = getCookie('refresh');
    if (authToken && refreshToken) {
        initialState = {
            isLoggedIn: true,
            access: authToken,
            refresh: refreshToken
        }
    } else {
        initialState = {
            isLoggedIn: false,
            access: '',
            refresh: '',
            user: {}
        }
   }
} else {
   initialState = {
       isLoggedIn: false,
       access: '',
       refresh: '',
       user: {}
   };
}

const auth = (state = initialState, action: AnyAction) => {
   switch (action.type) {
       case authConst.DEAUTHENTICATE:
           remCookie("access");
           remCookie("refresh");
           return {
               isLoggedIn: false
           };


       case authConst.AUTHENTICATE:
           const authObj = {
               isLoggedIn: true,
               access: action.payload.access,
               refresh: action.payload.refresh
           };
           console.log( action.payload.access);
           console.log(action.payload.refresh);
           setCookie("access", action.payload.access);
           setCookie("refresh", action.payload.refresh);
           return authObj;
        
       case authConst.RESTORE_AUTH_STATE:
           return {
               isLoggedIn: true,
               user: action.payload.user
           };
       default:
           return state;
   }
};

export default auth;
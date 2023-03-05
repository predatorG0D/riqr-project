import cookie from 'js-cookie';

export const setCookie = (name: string, data: CookieItem) => {
    cookie.set(name, data.value, {
        expires: data.expires,
    });
}

export const remCookie = (name: string) => cookie.remove(name);

export const getCookie = (key: string, req?: CookieRequest) => {
    return process.browser
        ? getCookieFromBrowser(key)
        : getCookieFromServer(key, req);
 };
 
 
const getCookieFromBrowser = (key: string) => {
    return cookie.get(key);
};
 
 
const getCookieFromServer = (key: string, req?: CookieRequest) => {
    if (!req?.headers.cookie) {
        return undefined;
    }
    const rawCookie = req.headers.cookie
        .split(';')
        .find(c => c.trim().startsWith(`${key}=`));
    if (!rawCookie) {
        return undefined;
    }
    return rawCookie.split('=')[1];
 };

interface CookieRequest {
     headers: {cookie: string};
 }

interface CookieItem {
    expires: number | Date | undefined;
    value: string | object;
}
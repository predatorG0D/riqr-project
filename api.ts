import { Method } from 'axios'

const defaultUrl = 'https://riqr-v1.herokuapp.com/api/';

export const configWithAuth = (method: Method, url:string, data = {}, token: string) => ({
    method,
    url: `${defaultUrl}${url}`,
    data,
    headers: {
        'Authorization': `Bearer ${token}`
    },
    withCredentials: true
})

export const configReq = (method: Method, url: string, data = {}) => ({
    method,
    url: `${defaultUrl}${url}`,
    data,
    withCredentials: true
})

export const configImageReq = (method: Method, url: string, data = new FormData(), token: string) => ({
    method,
    url: `${defaultUrl}${url}`,
    data,
    withCredentials: true,
    headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${token}`
    }
})


import { get, writable } from 'svelte/store';
import { AuthApi, UserApi, Configuration } from '../openapi';

export const accessToken=writable("")

async function getAccessToken(){
    return "Bearer "+get(accessToken)
}

const apiConfig=new Configuration({
    basePath: "/api/v1",
    accessToken: getAccessToken
})

export const authAPI = new AuthApi(apiConfig);
export const userAPI = new UserApi(apiConfig);
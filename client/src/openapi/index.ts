/* tslint:disable */

import { get, writable } from 'svelte/store';
import { AuthApi, UserApi } from './apis';
import { Configuration } from './runtime';

/* eslint-disable */
export * from './runtime';
export * from './apis';
export * from './models';

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
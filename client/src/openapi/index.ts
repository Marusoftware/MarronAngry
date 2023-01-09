/* tslint:disable */

import { AuthApi, DefaultApi, UserApi } from './apis';
import { Configuration } from './runtime';

/* eslint-disable */
export * from './runtime';
export * from './apis';
export * from './models';

const apiConfig=new Configuration({
    basePath: "/api/v1"
})

export const API = new DefaultApi(apiConfig);
export const authAPI = new AuthApi(apiConfig);
export const userAPI = new UserApi(apiConfig);
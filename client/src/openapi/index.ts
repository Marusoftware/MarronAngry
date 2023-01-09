/* tslint:disable */

import { AuthApi, UserApi } from './apis';
import { Configuration } from './runtime';

/* eslint-disable */
export * from './runtime';
export * from './apis';
export * from './models';

const apiConfig=new Configuration({
    basePath: "/api/v1"
})

export const authAPI = new AuthApi(apiConfig);
export const userAPI = new UserApi(apiConfig);
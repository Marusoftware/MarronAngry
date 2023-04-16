import { get, writable } from 'svelte/store';
import { AuthApi, UserApi, Configuration, OrganizationApi, type ResponseContext, ProjectApi, TaskApi, type Token } from '../openapi';
import type { Middleware } from '../openapi';

interface Notification {
    id?:number,
    kind:"info"|"warn",
    title:string,
    subtitle?: string,
    caption?: string,
    timeout?: number
}

export const tokens=writable<Token[]>([])
export const notifications=writable<Notification[]>([])

export function showNotification(notification:Notification){
    const defaults={
        id :Math.floor(Math.random() * 10000),
        subtitle: "",
        caption: "",
        timeout:0
    }
    notifications.update((all) =>[{
        ...defaults,
        ...notification
    }, ...all])
    return defaults.id
}

export const destroyNotification = (id:number) => {
    notifications.update((all) => all.filter((t) => t.id !== id))
  }

async function getAccessToken(){
    const ts=get(tokens)
    if(ts.length){
        return "Bearer "+ts[0].accessToken
    } else {
        return ""
    }
}

class APIExceptionHandlerMiddleware implements Middleware{
    async post(context: ResponseContext): Promise<void | Response> {
        try {
            const json=await context.response.json()
            if (json.detail) {
                showNotification({
                    kind:"warn",
                    title:json.detail,
                    subtitle: json.description??""
                })
            }
        } catch (error) {
            console.log(error)
        }
    }
}

const apiConfig=new Configuration({
    basePath: "/api/v1",
    accessToken: getAccessToken,
    middleware:[
        new APIExceptionHandlerMiddleware
    ]
})

export const authAPI = new AuthApi(apiConfig);
export const userAPI = new UserApi(apiConfig);
export const organizationAPI = new OrganizationApi(apiConfig);
export const projectAPI = new ProjectApi(apiConfig);
export const taskAPI = new TaskApi(apiConfig);
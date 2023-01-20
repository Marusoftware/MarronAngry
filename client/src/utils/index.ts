import { get, writable } from 'svelte/store';
import { AuthApi, UserApi, Configuration, OrganizationApi } from '../openapi';

interface Notification {
    id?:number,
    kind:"info"|"warn",
    title:string,
    subtitle?: string,
    caption?: string,
    timeout?: number
}

export const accessToken=writable("")
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
    return "Bearer "+get(accessToken)
}

const apiConfig=new Configuration({
    basePath: "/api/v1",
    accessToken: getAccessToken
})

export const authAPI = new AuthApi(apiConfig);
export const userAPI = new UserApi(apiConfig);
export const organizationAPI = new OrganizationApi(apiConfig);
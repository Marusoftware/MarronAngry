import { accessToken, organizationAPI, userAPI } from ".";
import { writable } from "svelte/store";
import type { Organization, User } from "../openapi";

export const user=writable<User>()
export const organizations=writable<Organization[]>([])

accessToken.subscribe(async (value)=>{
    if(value){
        user.set(await userAPI.userMe())
        organizations.set(await organizationAPI.organizationGetUs())
    }
})
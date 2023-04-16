import { tokens, organizationAPI, userAPI } from ".";
import { writable } from "svelte/store";
import type { Organization, User } from "../openapi";

export const user=writable<User>()
export const organizations=writable<Organization[]>([])

tokens.subscribe(async (value)=>{
    if(value.length){
        user.set(await userAPI.userMe())
        organizations.set(await organizationAPI.organizationGetUs())
    }else{
        user.set(undefined)
        organizations.set([])
    }
})
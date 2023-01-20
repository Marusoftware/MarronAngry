import { accessToken, userAPI } from ".";
import { writable } from "svelte/store";
import type { User } from "../openapi";

export const user=writable<User>()

accessToken.subscribe(async (value)=>{
    if(value){
        user.set(await userAPI.userMe())
    }
})
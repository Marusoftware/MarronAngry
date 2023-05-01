<script lang="ts">
    import { Label, Input, Helper } from "flowbite-svelte"
    import type { InputType } from "flowbite-svelte/types";
    import { Eye, EyeSlash } from "svelte-heros-v2";
    import { onMount } from "svelte";
    import type { Writable } from "svelte/store";
    import type { Field } from "svelte-forms/types";
    import { filterMessage } from "../utils";
    export let label:string=""
    export let store:Omit<Writable<Field<string>>, "set"> & {
        validate: () => Promise<Field<string>>;
        reset: () => void;
        clear: () => void;
        set(this: void, value: string | Field<string>): void;
    };
    export let type:InputType="text"
    export let placeholder=""
    let password:boolean=false

    onMount(()=>{
        if(type=="password"){
            password=true
        } else{
            password=false
        }
    })

    function changeVisible(e:Event){
        e.preventDefault()
        if(type=="password"){
            type="text"
        } else {
            type="password"
        }
    }
</script>

<div class="mb-6">
    <Label for={label.toLowerCase()} color={$store.invalid ? "red" : "gray"} class="block mb-2" >{label}</Label>
    <Input id={label.toLowerCase()} bind:type={type} bind:value={$store.value} color={$store.invalid ? "red" : "base"} placeholder={placeholder} {...$$props} >
        <svelte:fragment slot="right">
            {#if password}
                <button on:click={changeVisible} type="button">
                    {#if type=="password"}
                    <EyeSlash />
                    {:else}
                    <Eye />
                    {/if}
                </button>
            {/if}
        </svelte:fragment>
    </Input>
    {#if $store.invalid}
    <Helper color={$store.invalid ? "red" : "gray"} >{filterMessage($store.errors.join(", "))}</Helper>
    {/if}
</div>

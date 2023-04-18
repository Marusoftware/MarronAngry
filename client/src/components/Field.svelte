<script lang="ts">
    import { Label, Input, Helper } from "flowbite-svelte"
    import type { InputType } from "flowbite-svelte/types";
    import { Eye, EyeSlash } from "svelte-heros-v2";
    import { onMount } from "svelte";
    export let labelText=""
    export let invalidText=""
    export let invalid=false
    export let value: string | number
    export let id:string=""
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
    <Label for={id} color={invalid ? "red" : "gray"} class="block mb-2" >{labelText}</Label>
    <Input id={id} bind:type={type} bind:value={value} color={invalid ? "red" : "base"} placeholder={placeholder} {...$$props} >
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
    {#if invalid}
    <Helper color={invalid ? "red" : "gray"} >{invalidText}</Helper>
    {/if}
</div>

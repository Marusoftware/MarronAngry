<script lang="ts">
    import { Label, Input, Helper } from "flowbite-svelte"
    import type { InputType } from "flowbite-svelte/types";
    export let labelText=""
    export let invalidText=""
    export let invalid=false
    export let value: string | number
    export let id:string=""
    export let type:InputType="text"
    export let placeholder=""
</script>

<div class="mb-6">
    <Label for={id} color={invalid ? "red" : "gray"} class="block mb-2" >{labelText}</Label>
    <Input id={id} type={type} bind:value={value} color={invalid ? "red" : "base"} placeholder={placeholder} ></Input>
    {#if invalid}
    <Helper color={invalid ? "red" : "gray"} >{invalidText}</Helper>
    {/if}
</div>

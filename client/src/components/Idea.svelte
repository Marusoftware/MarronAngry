<script lang="ts">
    import { Button, Heading, Label, Modal, Select, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Tooltip } from "flowbite-svelte";
    import { createEventDispatcher, onMount } from "svelte";
    import { field, form } from "svelte-forms";
    import { pattern, required } from "svelte-forms/validators";
    import type { Idea } from "../openapi";
    import { ideaAPI } from "../utils";
    import Field from "./Field.svelte";
    const dispatch=createEventDispatcher()

    export let idea:Idea={id:"", name:"", description:"", projectId:""}
    let name = field('name', "", [required()])
    let description = field('description', "", [required()])
    const updateForm = form(name, description)

    export let open = false;

    $:{
        $name.value=idea.name
        $description.value=idea.description
    }
    async function submit(e:Event){
        e.preventDefault()
        await updateForm.validate()
        if(!$updateForm.valid){
            return
        }
        if (idea.id){
            idea=await ideaAPI.ideaUpdate({
                ideaId:idea.id,
                ideaUpdate:{
                    name:$name.value,
                    description:$description.value,
                    projectId:idea.projectId,
                }
            })
            open=false
        }else{
            idea=await ideaAPI.ideaCreate({
                ideaCreate:{
                    name:$name.value,
                    description:$description.value,
                    projectId:idea.projectId
                }
            })
        }
        dispatch("close", idea)
    }
</script>

<Modal bind:open title="Idea">
    {#if idea.id}
        <Heading>Update Idea</Heading>
    {:else}
        <Heading>Create Idea</Heading>
    {/if}
    <form on:submit={submit}>
        <Field type="text" label="Name" placeholder="Enter name..." bind:store={name} />
        <Field type="text" label="Description" placeholder="Enter description..." bind:store={description} />
    </form>
    <svelte:fragment slot="footer">
        <Button on:click={submit} disabled={!$updateForm.valid}>{#if idea.id}変更{:else}作成{/if}</Button>
    </svelte:fragment>
</Modal>
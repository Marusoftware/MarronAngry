<script lang="ts">
    import { Button, Heading, Modal } from "flowbite-svelte";
    import { createEventDispatcher } from "svelte";
    import { field, form } from "svelte-forms";
    import { required } from "svelte-forms/validators";
    import type { Project } from "../openapi";
    import { projectAPI } from "../utils";
    import { organizations } from "../utils/store";
    import Field from "./Field.svelte";
    const dispatch=createEventDispatcher()

    export let project:Project={id:"", name:"",description:"", organizationId:"", members:[]};
    const name = field('name', "", [required()])
    const description = field('description', "", [required()])
    const updateForm = form(name, description)

    export let open = false;

    $:{
        $name.value=project.name
        $description.value=project.description
    }
    async function submit(e:Event){
        e.preventDefault()
        await updateForm.validate()
        if(!$updateForm.valid){
            return
        }
        if (project.id){
            project=await projectAPI.projectUpdate({
                projId:project.id,
                projectUpdate:{
                    name:$name.value,
                    description:$description.value,
                    organizationId:$organizations[0].id
                }
            })
            open=false
        }else{
            project=await projectAPI.projectCreate({
                projectCreate:{
                    name:$name.value,
                    description:$description.value,
                    organizationId:$organizations[0].id
                }
            })
        }
        dispatch("close", project)
    }
</script>

<Modal bind:open title="Project">
    {#if project.id}
        <Heading>Update Project</Heading>
    {:else}
        <Heading>Create Project</Heading>
    {/if}
    <form on:submit={submit}>
        <Field id="name" type="text" labelText="Name" placeholder="Enter name..." bind:value={$name.value} invalid={$name.invalid} invalidText={$name.errors.join(", ")} />
        <Field id="description" type="text" labelText="Description" placeholder="Enter description..." bind:value={$description.value} invalid={$description.invalid} invalidText={$description.errors.join(", ")} />
    </form>
    <svelte:fragment slot="footer">
        <Button on:click={submit} disabled={!$updateForm.valid}>{#if project.id}変更{:else}作成{/if}</Button>
    </svelte:fragment>
</Modal>
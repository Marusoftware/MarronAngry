<script lang="ts">
    import { Button, Heading, Modal } from "flowbite-svelte";
    import { createEventDispatcher } from "svelte";
    import { field, form } from "svelte-forms";
    import { required } from "svelte-forms/validators";
    import type { Organization } from "../openapi";
    import { organizationAPI } from "../utils";
    import Field from "./Field.svelte";
    const dispatch=createEventDispatcher()

    export let organization:Organization={id:"", name:"",description:"", members:[]};
    const name = field('name', "", [required()])
    const description = field('description', "", [required()])
    const updateForm = form(name, description)

    export let open = false;

    $:{
        $name.value=organization.name
        $description.value=organization.description
    }
    async function submit(e:Event){
        e.preventDefault()
        await updateForm.validate()
        if(!$updateForm.valid){
            return
        }
        if (organization.id){
            organization=await organizationAPI.organizationUpdate({
                orgId:organization.id,
                organizationUpdate:{
                    name:$name.value,
                    description:$description.value
                }
            })
        }else{
            organization=await organizationAPI.organizationCreate({
                organizationCreate:{
                    name:$name.value,
                    description:$description.value
                }
            })
        }
        dispatch("close", organization)
    }

</script>

<Modal bind:open title="Organization">
    {#if organization.id}
        <Heading>Update Organization</Heading>
    {:else}
        <Heading>Create Organization</Heading>
    {/if}
    <form on:submit={submit}>
        <Field id="name" type="text" labelText="Name" placeholder="Enter name..." bind:value={$name.value} invalid={$name.invalid} invalidText={$name.errors.join(", ")} />
        <Field id="description" type="text" labelText="Description" placeholder="Enter description..." bind:value={$description.value} invalid={$description.invalid} invalidText={$description.errors.join(", ")} />
    </form>
    <svelte:fragment slot="footer">
        <Button on:click={submit} disabled={!$updateForm.valid}>{#if organization.id}変更{:else}作成{/if}</Button>
    </svelte:fragment>
</Modal>
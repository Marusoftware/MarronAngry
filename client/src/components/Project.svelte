<script lang="ts">
    import { Button, Heading, Modal, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Tooltip } from "flowbite-svelte";
    import { createEventDispatcher } from "svelte";
    import { field, form } from "svelte-forms";
    import { pattern, required } from "svelte-forms/validators";
    import type { Project } from "../openapi";
    import { projectAPI, userAPI } from "../utils";
    import { organizations } from "../utils/store";
    import Field from "./Field.svelte";
    const dispatch=createEventDispatcher()

    export let project:Project={id:"", name:"",description:"", organizationId:"", members:[]};
    const name = field('name', "", [required()])
    const description = field('description', "", [required()])
    const updateForm = form(name, description)
    const member=field("member","",[pattern(/([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})/)])
    const memberForm = form(member)

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
    async function addMember() {
        await memberForm.validate()
        if(!$memberForm.valid){
            return
        }
        const orgMember=await projectAPI.projectAddUser({
            projId:project.id,
            userId:$member.value
        })
        project.members=[...project.members, orgMember]
    }
    async function deleteMember(userId:string) {
        await projectAPI.projectDelUser({
            projId:project.id,
            userId:userId
        })
        project.members=project.members.filter((value)=>value.userId!==userId)
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
    {#if project.id}
    <Table>
        <TableHead>
            <TableHeadCell>User name</TableHeadCell>
            <TableHeadCell>Permission</TableHeadCell>
            <TableHeadCell></TableHeadCell>
        </TableHead>
        <TableBody>
            {#each project.members as member (member.id)}
            <TableBodyRow>
                <TableBodyCell>
                    <div id={member.id}>
                    {#await userAPI.userGet({id:member.userId})}
                        Getting Username...
                    {:then user}
                        {user.name}
                    {/await}
                    </div>
                    <Tooltip triggeredBy="#{member.id}">{member.userId}</Tooltip>
                </TableBodyCell>
                <TableBodyCell>{member.isAdmin ? "Admin":"Member"}</TableBodyCell>
                <TableBodyCell><Button on:click={async ()=>{await deleteMember(member.userId)}}>Delete</Button></TableBodyCell>
            </TableBodyRow>
            {/each}
        </TableBody>
    </Table>
    <Field id="uid" type="text" labelText="UserID" placeholder="Enter UserID..." bind:value={$member.value} invalid={$member.invalid} invalidText={$member.errors.join(", ")} ></Field><Button on:click={addMember}>Add member</Button>
    {/if}
    <svelte:fragment slot="footer">
        <Button on:click={submit} disabled={!$updateForm.valid}>{#if project.id}変更{:else}作成{/if}</Button>
    </svelte:fragment>
</Modal>
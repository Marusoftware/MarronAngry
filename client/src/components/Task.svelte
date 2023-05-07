<script lang="ts">
    import { Button, Heading, Label, Modal, Select, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Tooltip } from "flowbite-svelte";
    import { createEventDispatcher, onMount } from "svelte";
    import { field, form } from "svelte-forms";
    import { pattern, required } from "svelte-forms/validators";
    import type { Task } from "../openapi";
    import { taskAPI, userAPI } from "../utils";
    import Field from "./Field.svelte";
    const dispatch=createEventDispatcher()

    export let task:Task={id:"", name:"", description:"", projectId:"", start:new Date(), end:new Date(), members:[]}
    let name = field('name', "", [required()])
    let description = field('description', "", [required()])
    let date = field('date', "", [required()])
    let date2 = field('date2', "", [required()])
    const updateForm = form(name, description, date, date2)
    let member=field("member","",[pattern(/([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})/)])
    const memberForm = form(member)

    export let open = false;

    $:{
        $name.value=task.name
        $description.value=task.description
        $date.value=task.start.toISOString().slice(0, 16)
        $date2.value=task.start.toISOString().slice(0, 16)
    }
    async function submit(e:Event){
        e.preventDefault()
        await updateForm.validate()
        if(!$updateForm.valid){
            return
        }
        if (task.id){
            task=await taskAPI.taskUpdate({
                taskId:task.id,
                taskUpdate:{
                    name:$name.value,
                    description:$description.value,
                    projectId:task.projectId,
                    start:new Date($date.value),
                    end:new Date($date2.value)
                }
            })
            open=false
        }else{
            task=await taskAPI.taskCreate({
                taskCreate:{
                    name:$name.value,
                    description:$description.value,
                    projectId:task.projectId,
                    start:new Date($date.value),
                    end:new Date($date2.value)
                }
            })
        }
        dispatch("close", task)
    }
    async function addMember() {
        await memberForm.validate()
        if(!$memberForm.valid){
            return
        }
        const orgMember=await taskAPI.taskAddUser({
            taskId:task.id,
            userId:$member.value
        })
        task.members=[...task.members, orgMember]
    }
    async function deleteMember(userId:string) {
        await taskAPI.taskDelUser({
            taskId:task.id,
            userId:userId
        })
        task.members=task.members.filter((value)=>value.userId!==userId)
    }
</script>

<Modal bind:open title="Task">
    {#if task.id}
        <Heading>Update Task</Heading>
    {:else}
        <Heading>Create Task</Heading>
    {/if}
    <form on:submit={submit}>
        <Field type="text" label="Name" placeholder="Enter name..." bind:store={name} />
        <Field type="text" label="Description" placeholder="Enter description..." bind:store={description} />
        <Field type="datetime-local" label="Start Date" placeholder="Enter Date..." bind:store={date} />
        <Field type="datetime-local" label="End Date" placeholder="Enter Date..." bind:store={date2} />
    </form>
    {#if task.id}
    <Table>
        <TableHead>
            <TableHeadCell>User name</TableHeadCell>
            <TableHeadCell>Permission</TableHeadCell>
            <TableHeadCell></TableHeadCell>
        </TableHead>
        <TableBody>
            {#each task.members as member (member.id)}
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
    <Field type="text" label="UserID" placeholder="Enter UserID..." bind:store={member} /><Button on:click={addMember}>Add member</Button>
    {/if}
    <svelte:fragment slot="footer">
        <Button on:click={submit} disabled={!$updateForm.valid}>{#if task.id}変更{:else}作成{/if}</Button>
    </svelte:fragment>
</Modal>
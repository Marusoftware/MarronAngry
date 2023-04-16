<script lang="ts">
    import { Button, Heading, Label, Modal, Select, Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell, Tooltip } from "flowbite-svelte";
    import { createEventDispatcher, onMount } from "svelte";
    import { field, form } from "svelte-forms";
    import { pattern, required } from "svelte-forms/validators";
    import type { Task } from "../openapi";
    import { projectAPI, taskAPI, userAPI } from "../utils";
    import { organizations } from "../utils/store";
    import Field from "./Field.svelte";
    const dispatch=createEventDispatcher()

    export let task:Task={id:"", name:"", description:"", projectId:"", time:new Date(), members:[]}
    const name = field('name', "", [required()])
    const description = field('description', "", [required()])
    const date = field('description', "", [required()])
    const updateForm = form(name, description)
    const member=field("member","",[pattern(/([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})/)])
    const memberForm = form(member)
    let projects=[]

    export let open = false;

    async function onOpen(open:boolean) {
        if(open){
            projects=(await projectAPI.projectGet({orgId:$organizations[0].id})).map((value)=>{return {name:value.name, value:value.id}})
            task.projectId=projects[0].value
        }
    }
    $: onOpen(open)

    $:{
        $name.value=task.name
        $description.value=task.description
        $date.value=task.time.toISOString().slice(0, 16)
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
                    time:new Date($date.value)
                }
            })
            open=false
        }else{
            task=await taskAPI.taskCreate({
                taskCreate:{
                    name:$name.value,
                    description:$description.value,
                    projectId:task.projectId,
                    time:new Date($date.value)
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
        <Field id="name" type="text" labelText="Name" placeholder="Enter name..." bind:value={$name.value} invalid={$name.invalid} invalidText={$name.errors.join(", ")} />
        <Field id="description" type="text" labelText="Description" placeholder="Enter description..." bind:value={$description.value} invalid={$description.invalid} invalidText={$description.errors.join(", ")} />
        <Field id="date" type="datetime-local" labelText="Date" placeholder="Enter Date..." bind:value={$date.value} />
        <Label>Project
            <Select class="mt-2" items={projects} bind:value={task.projectId} />
        </Label>
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
    <Field id="uid" type="text" labelText="UserID" placeholder="Enter UserID..." bind:value={$member.value} invalid={$member.invalid} invalidText={$member.errors.join(", ")} ></Field><Button on:click={addMember}>Add member</Button>
    {/if}
    <svelte:fragment slot="footer">
        <Button on:click={submit} disabled={!$updateForm.valid}>{#if task.id}変更{:else}作成{/if}</Button>
    </svelte:fragment>
</Modal>
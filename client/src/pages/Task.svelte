<script lang="ts">
    import {
      Button,
      Heading,
      Table,
      TableBody,
      TableBodyCell,
      TableBodyRow,
      TableHead,
      TableHeadCell,
    } from "flowbite-svelte";
    import Task from "../components/Task.svelte";
    import { accessToken, projectAPI, taskAPI } from "../utils";
    import type { Task as TaskModel, Project } from "../openapi"
    import { onMount } from "svelte";
    import { organizations } from "../utils/store";
    let open = false;
    let taskModal:TaskModel={id:"", name:"", description:"", projectId:"", time:new Date(), members:[]}
    let tasks:TaskModel[]=[]
  
    async function updateTable() {
      tasks=[];
      (await projectAPI.projectGet({orgId:$organizations[0].id})).forEach(async (project:Project) => {
        tasks=[...tasks, ...await taskAPI.taskGet({prjId:project.id})]
      })
    }
  
    onMount(async () => {
      await updateTable()
    })
  </script>
  
  <Task bind:open task={taskModal} on:close={updateTable} />
  
  <Heading>Task</Heading>
  {#if $accessToken}
    <Heading tag="h2">Your Task</Heading>
    <Button
      on:click={() => {
        taskModal = {id:"", name:"", description:"", projectId:"", time:new Date(), members:[]};
        open = true;
      }}>Add Task</Button
    ><br />
    <Table>
      <TableHead>
        <TableHeadCell>Name</TableHeadCell>
        <TableHeadCell>Description</TableHeadCell>
        <TableHeadCell>Time</TableHeadCell>
        <TableHeadCell />
      </TableHead>
      <TableBody>
        {#each tasks as task}
          <TableBodyRow>
            <TableBodyCell>{task.name}</TableBodyCell>
            <TableBodyCell>{task.description}</TableBodyCell>
            <TableBodyCell>{task.time}</TableBodyCell>
            <TableBodyCell>
              <Button
                on:click={() => {
                  taskModal = task
                  open = true;
                }}
              >Edit</Button>
              <Button on:click={async ()=>{await taskAPI.taskDelete({taskId:task.id});await updateTable() }}>Delete</Button>
            </TableBodyCell>
          </TableBodyRow>
        {:else}
          You have NO Tasks.
        {/each}
      </TableBody>
    </Table>
  {/if}
  
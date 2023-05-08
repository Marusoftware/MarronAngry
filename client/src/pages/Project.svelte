<script lang="ts">
  import {
    Button,
    Fileupload,
    Heading,
    TabItem,
    Table,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
    Tabs,
  } from "flowbite-svelte";
  import Task from "../components/Task.svelte";
  import { fileAPI, ideaAPI, projectAPI, taskAPI } from "../utils";
  import type { Project, Task as TaskModel, Idea as IdeaModel } from "../openapi"
  import { onMount } from "svelte";
    import { organizations } from "../utils/store";
    import Idea from "../components/Idea.svelte";
  let files:FileList;
  let open = false;
  let open2 = false;
  let path="/";
  let taskModal:TaskModel={id:"", name:"", description:"", projectId:"", start:new Date(), end:new Date(), members:[]}
  let ideaModal:IdeaModel={id:"", name:"", description:"", projectId:""}
  let tasks:TaskModel[]=[]
  let ideas:IdeaModel[]=[]
  export let pid:string;
  let project:Project={id:"", name:"", description:"", organizationId:"", members:[]}
  async function updateTable() {
    tasks=await taskAPI.taskGet({prjId:pid})
    project=(await projectAPI.projectGet({orgId:$organizations[0].id})).filter((v)=>v.id===pid)[0]
  }
  async function updateTable2() {
    ideas=await ideaAPI.ideaGet({prjId:pid})
  }

  async function init(stub=undefined) {
    await updateTable()
    await updateTable2()
  }

  $: init(pid).then()
  
  onMount(init)
  function uppath(e:Event) {
    e.preventDefault()
    let lst=path.split("/")
    lst.pop()
    path=lst.join("/")
  }
</script>

<Task bind:open task={taskModal} on:close={updateTable} />
<Idea bind:open={open2} idea={ideaModal} on:close={updateTable2} />

<Heading>Project {project.name}</Heading>
<Tabs>
  <TabItem title="Task" open>
    <Button
  on:click={() => {
    taskModal = {id:"", name:"", description:"", projectId:pid, start:new Date(), end:new Date(), members:[]};
    open = true;
  }}>Add Task</Button
><br />
<Table>
  <TableHead>
    <TableHeadCell>Name</TableHeadCell>
    <TableHeadCell>Description</TableHeadCell>
    <TableHeadCell>Start Time</TableHeadCell>
    <TableHeadCell>End Time</TableHeadCell>
    <TableHeadCell />
  </TableHead>
  <TableBody>
    {#each tasks as task}
      <TableBodyRow>
        <TableBodyCell>{task.name}</TableBodyCell>
        <TableBodyCell>{task.description}</TableBodyCell>
        <TableBodyCell>{task.start}</TableBodyCell>
        <TableBodyCell>{task.end}</TableBodyCell>
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
  </TabItem>
  <TabItem title="Idea" open>
    <Button
  on:click={() => {
    ideaModal = {id:"", name:"", description:"", projectId:pid};
    open2 = true;
  }}>Add Idea</Button
><br />
<Table>
  <TableHead>
    <TableHeadCell>Name</TableHeadCell>
    <TableHeadCell>Description</TableHeadCell>
    <TableHeadCell />
  </TableHead>
  <TableBody>
    {#each ideas as idea}
      <TableBodyRow>
        <TableBodyCell>{idea.name}</TableBodyCell>
        <TableBodyCell>{idea.description}</TableBodyCell>
        <TableBodyCell>
          <Button
            on:click={() => {
              ideaModal=idea
              open2 = true;
            }}
          >Edit</Button>
          <Button on:click={async ()=>{await ideaAPI.ideaDelete({ideaId:idea.id});await updateTable2() }}>Delete</Button>
        </TableBodyCell>
      </TableBodyRow>
    {:else}
      You have NO Ideas.
    {/each}
  </TableBody>
</Table>
  </TabItem>
  <TabItem title="Files">
    <Fileupload on:change={async (e)=>{e.preventDefault(); await fileAPI.filePut({prjId:pid,fullPath:path+"/"+e.target.files[0].name, file:e.target.files[0]}); path=path}} />
    <Table>
      <TableHead>
        <TableHeadCell>Filename</TableHeadCell>
      </TableHead>
      <TableBody>
        {#if path!=="/"}
        <TableBodyRow>
          <TableBodyCell><button class="font-medium text-blue-600 hover:underline dark:text-blue-500" on:click={uppath}>..</button></TableBodyCell>
        </TableBodyRow>
        {/if}
        {#await fileAPI.fileLs({prjId:pid, fullPath:path}) then files} 
      {#each files as file}
      <TableBodyRow>
        <TableBodyCell><button class="font-medium text-blue-600 hover:underline dark:text-blue-500" on:click={(e)=>{e.preventDefault();path+="/"+file}}>{file}</button></TableBodyCell>
      </TableBodyRow>
      {/each}
    {/await}
      </TableBody>
    </Table>
    
  </TabItem>
</Tabs>

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
    import Project from "../components/Project.svelte";
    import { accessToken, projectAPI } from "../utils";
    import type { Project as ProjectModel} from "../openapi"
    import { onMount } from "svelte";
    import { organizations } from "../utils/store";
    let open = false;
    let projectModal:ProjectModel={id:"", name:"", description:"", organizationId:""}
    let projects:ProjectModel[]=[]
  
    async function updateTable() {
      projects=await projectAPI.projectGet({orgId:$organizations[0].id})
    }
  
    onMount(async () => {
      await updateTable()
    })
  </script>
  
  <Project bind:open project={projectModal} on:close={updateTable} />
  
  <Heading>Projects</Heading>
  {#if $accessToken}
    <Heading tag="h2">Your Projects</Heading>
    <Button
      on:click={() => {
        projectModal = {id:"", name:"",description:"", organizationId:""};
        open = true;
      }}>Add Project</Button
    ><br />
    <Table>
      <TableHead>
        <TableHeadCell>Name</TableHeadCell>
        <TableHeadCell>Description</TableHeadCell>
        <TableHeadCell />
      </TableHead>
      <TableBody>
        {#each projects as project}
          <TableBodyRow>
            <TableBodyCell>{project.name}</TableBodyCell>
            <TableBodyCell>{project.description}</TableBodyCell>
            <TableBodyCell>
              <Button
                on:click={() => {
                  projectModal = project
                  open = true;
                }}
              >Edit</Button>
              <Button on:click={async ()=>{await projectAPI.projectDelete({projId:project.id});await updateTable() }}>Delete</Button>
            </TableBodyCell>
          </TableBodyRow>
        {:else}
          You have NO Projects.
        {/each}
      </TableBody>
    </Table>
  {/if}
  
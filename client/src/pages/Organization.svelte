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
  import Organization from "../components/Organization.svelte";
  import { accessToken, organizationAPI } from "../utils";
  import type {Organization as OrganizationModel} from "../openapi"
    import { onMount } from "svelte";
  let organizationModal = {id:"", name:"",description:"", members:[]};
  let open = false;
  let organizations:OrganizationModel[]=[]

  async function updateTable() {
    organizations=await organizationAPI.organizationGetUs()
  }

  onMount(async () => {
    await updateTable()
  })
</script>

<Organization bind:open organization={organizationModal} on:close={updateTable} />

<Heading>Organization</Heading>
{#if $accessToken}
  <Heading tag="h2">Your Organization</Heading>
  <Button
    on:click={() => {
      organizationModal = {id:"", name:"",description:"", members:[]};
      open = true;
    }}>Add Organization</Button
  ><br />
  <Table>
    <TableHead>
      <TableHeadCell>Name</TableHeadCell>
      <TableHeadCell>Description</TableHeadCell>
      <TableHeadCell />
    </TableHead>
    <TableBody>
      {#each organizations as organization}
        <TableBodyRow>
          <TableBodyCell>{organization.name}</TableBodyCell>
          <TableBodyCell>{organization.description}</TableBodyCell>
          <TableBodyCell>
            <Button
              on:click={() => {
                organizationModal = organization;
                open = true;
              }}
            >Edit</Button>
            <Button on:click={async ()=>{await organizationAPI.organizationDelete({orgId:organization.id});updateTable() }}>Delete</Button>
          </TableBodyCell>
        </TableBodyRow>
      {:else}
        You have NO Organizations.
      {/each}
    </TableBody>
  </Table>
{/if}

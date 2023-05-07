<script lang="ts">
import { Sidebar, SidebarGroup, SidebarItem, SidebarWrapper, SidebarDropdownItem, SidebarDropdownWrapper, Avatar, Button } from 'flowbite-svelte';
import { projectAPI } from '../utils';
import { organizations } from '../utils/store';
import { navigate } from 'svelte-routing';

function updateOrganization(id:string) {
  organizations.update((value)=>{
    value.unshift(value.splice(value.findIndex((v)=>v.id===id), 1)[0])
    return value
  })
}
</script>

<Sidebar>
  <SidebarWrapper>
    <SidebarGroup>
    {#each $organizations as org (org.id)}
    <SidebarDropdownWrapper isOpen label={org.name}>
      <svelte:fragment slot="icon">
        <Avatar rounded />
      </svelte:fragment>
      {#await projectAPI.projectGet({orgId:org.id}) }
        <SidebarDropdownItem label="Getting Project Info..." />
      {:then prjs}
      {#each prjs as prj}
        <SidebarDropdownItem label={prj.name} on:click={(e)=>{e.preventDefault();navigate("/project/"+prj.id)}}/>
      {/each}
      {/await}
      <SidebarDropdownItem label="Manage Projects" on:click={(e)=>{e.preventDefault();updateOrganization(org.id);navigate("/project")}}/>
    </SidebarDropdownWrapper>
    {/each}
    </SidebarGroup>
  </SidebarWrapper>
  <SidebarItem label="Manage Organizations" on:click={(e)=>{e.preventDefault();navigate("/organization")}} />
</Sidebar>
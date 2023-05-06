<script lang="ts">
import { Sidebar, SidebarGroup, SidebarItem, SidebarWrapper, SidebarDropdownItem, SidebarDropdownWrapper, Avatar } from 'flowbite-svelte';
import { organizationAPI, projectAPI } from '../utils';
</script>
<Sidebar>
  <SidebarWrapper>
    <SidebarGroup>
    {#await organizationAPI.organizationGetUs()}
    <SidebarItem label="Getting Organization Info..." />
    {:then orgs}
    {#each orgs as org (org.id)}
    <SidebarDropdownWrapper label={org.name}>
      <svelte:fragment slot="icon">
        <Avatar />
      </svelte:fragment>
      {#await projectAPI.projectGet({orgId:org.id}) }
      <SidebarDropdownItem label="Getting Project Info..." />
      {:then prjs}
        {#each prjs as prj}
          <SidebarDropdownItem label={prj.name} />
        {/each}
      {/await}
    </SidebarDropdownWrapper>
    {/each}
    {/await}
    </SidebarGroup>
  </SidebarWrapper>
</Sidebar>
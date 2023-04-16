<script lang="ts">
  import { 
    Navbar,
    NavBrand,
    NavHamburger,
    NavUl,
    NavLi,
    Avatar,
    Dropdown,
    DropdownHeader,
    DropdownItem,
    DropdownDivider,
    Button,
    DarkMode,
    Chevron,
    Radio
  } from "flowbite-svelte";
  import { Router, Route, navigate } from "svelte-routing";
  import { tokens, authAPI, destroyNotification, notifications, userAPI } from "./utils";
  import Home from "./pages/Home.svelte";
  import Signin from "./pages/Signin.svelte";
  import Signup from "./pages/Signup.svelte";
  import Notification from "./components/Notification.svelte";
  import { onMount } from "svelte";
  import Settings from "./pages/Settings.svelte";
  import { organizations, user } from "./utils/store";
  import Organization from "./pages/Organization.svelte";
  import Project from "./pages/Project.svelte";
  import Task from "./pages/Task.svelte";

  onMount(async () => {
    tokens.set(await authAPI.authSession())
  })
  async function signout() {
    await authAPI.authSignout()
    tokens.update((value)=> value.slice(1))
  }

  async function changeUser(token:string){
    tokens.update((value)=>{
      value.unshift(value.splice(value.findIndex((v)=>v.accessToken===token))[0])
      return value
    })
  }

  let organization:number=0
  function updateOrganizations(select:number) {
    $organizations=[$organizations[select], ...$organizations.filter((value, index)=>index!==select)]
    organization=0
  }
  $: updateOrganizations(organization)
</script>

<div class="bg-white dark:bg-gray-800 min-h-screen">
<Navbar let:hidden let:toggle>
  <NavBrand href="/">
    <img src="/marron.jpg" alt="Marron Logo" class="mr-3 h-6 sm:h-9" />
    <span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Marron</span>
  </NavBrand>
  <div class="flex items-center md:order-2">
    {#if $tokens.length}
      <Avatar id="avatar-menu" src="/images/profile-picture-3.webp" />
    {:else}
      <Button size="sm" on:click={() => navigate("/signin")} >サインイン</Button>
    {/if}
    <DarkMode />
    <NavHamburger on:click={toggle} class1="w-full md:flex md:w-auto md:order-1"/>
  </div>
  {#if $tokens.length}
  <Dropdown placement="bottom" triggeredBy="#avatar-menu">
    <DropdownHeader>
    <span class="block text-sm"> { $user.fullname }</span>
    <span class="block truncate text-sm font-medium"> { $user.email } </span>
    </DropdownHeader>
    <DropdownItem on:click={()=>{navigate("/settings")}}>Settings</DropdownItem>
    <DropdownDivider />
    <DropdownItem class="flex items-center justify-between"><Chevron placement="right">Switch Account</Chevron></DropdownItem>
    <Dropdown placement="left-start">
      {#each $tokens as token (token.accessToken)}
        {#if token.userId!==$tokens[0].userId}
        {#await userAPI.userGet({id:token.userId})}
        <DropdownItem>Getting user info...</DropdownItem>
        {:then user}
        <DropdownItem on:click={()=>{changeUser(token.accessToken)}}>
          <Avatar src="/images/profile-picture-3.webp" size="xs" />{user.name}
        </DropdownItem>
        {/await}
        {/if}
      {/each}
      <DropdownItem on:click={() => navigate("/signin")}>+ Add user</DropdownItem>
    </Dropdown>
    <DropdownItem on:click={signout}>Sign out</DropdownItem>
  </Dropdown>
  {/if}
  <NavUl {hidden}>
    <NavLi id="organization" href="#" on:click={() => navigate("/organization")}>Organization</NavLi>
    {#if $organizations}
      <Dropdown  placement="bottom" triggeredBy="#organization">
        {#each $organizations as org, i(org.id)}
          <li>
            <Radio name="organization-select" bind:group={organization} value={i}>{org.name}</Radio>
          </li>
        {/each}
      </Dropdown>
    {/if}
    <NavLi href="#" on:click={() => navigate("/project")}>Project</NavLi>
    <NavLi href="#" on:click={() => navigate("/task")}>Task</NavLi>
  </NavUl>
</Navbar>
<Router>
  <main class="container p-10 dark:text-white mx-auto">
    {#if $notifications}
    <div class="absolute top-20 right-5 w-full max-w-xs z-50 isolation">
      {#each $notifications as nortification (nortification.id)} 
        <Notification title={nortification.title} subtitle={nortification.subtitle} kind={nortification.kind}
        on:close={() => destroyNotification(nortification.id)} />
      {/each}
    </div>
    {/if}
    <Route path="" component={Home} />
    <Route path="/signin" component={Signin} />
    <Route path="/signin/:username" let:params>
      <Signin username={params.username} />
    </Route>
    <Route path="/signup" component={Signup} />
    <Route path="/settings" component={Settings} />
    <Route path="/organization" component={Organization} />
    <Route path="/project" component={Project} />
    <Route path="/task" component={Task} />
  </main>
</Router>
</div>
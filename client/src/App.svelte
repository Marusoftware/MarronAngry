<script lang="ts">
  import { 
    Navbar,
    NavHamburger,
    Avatar,
    Dropdown,
    DropdownHeader,
    DropdownItem,
    DropdownDivider,
    Button,
    DarkMode,
    Chevron,
  } from "flowbite-svelte";
  import NavBrand from "./components/NavBrand.svelte";
  import { Router, Route, navigate } from "svelte-routing";
  import { tokens, authAPI, destroyNotification, notifications, userAPI } from "./utils";
  import Home from "./pages/Home.svelte";
  import Signin from "./pages/Signin.svelte";
  import Signup from "./pages/Signup.svelte";
  import Notification from "./components/Notification.svelte";
  import Settings from "./pages/Settings.svelte";
  import { user } from "./utils/store";
  import Organization from "./pages/Organization.svelte";
  import ProjectManage from "./pages/ProjectManage.svelte";
  import Project from "./pages/Project.svelte";
    import { onMount } from "svelte";
    import ProjectSwitcher from "./components/ProjectSwitcher.svelte";

  onMount(async () => {
    tokens.set(await authAPI.authSession())
    if($tokens.length){
      try{
        logo=URL.createObjectURL(await userAPI.userMeLogo())
      } catch(e){
        logo=undefined
      }
    }
  })
  let logo="";
  async function signout() {
    await authAPI.authSignout()
    tokens.update((value)=> value.slice(1))
    if(!$tokens.length){
      location.href="/"
    }
    logo=undefined
  }

  async function changeUser(token:string){
    tokens.update((value)=>{
      value.unshift(value.splice(value.findIndex((v)=>v.accessToken===token), 1)[0])
      return value
    })
    try{
      logo=URL.createObjectURL(await userAPI.userMeLogo())
    } catch(e){
      logo=undefined
    }
  }

</script>

<div class="bg-white dark:bg-gray-800 min-h-screen">
<Navbar let:hidden let:toggle>
  <NavBrand on:click={()=>{navigate("/")}}>
    <img src="/marron.jpg" alt="Marron Logo" class="mr-3 h-6 sm:h-9" />
    <span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Marron</span>
  </NavBrand>
  <div class="flex items-center md:order-2 space-x-1">
    {#if $tokens.length}
      <div id="avatar-menu">
        <Avatar src={logo} />
      </div>
    {:else}
      <Button size="sm" on:click={() => navigate("/signin")} >サインイン</Button>
    {/if}
    <NavHamburger on:click={toggle} class1="w-full md:flex md:w-auto md:order-1"/>
    <DarkMode />
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
          {#await userAPI.userGetLogo({id:user.id}) then logo}
          <Avatar size="xs" src={URL.createObjectURL(logo)} />{user.name}
          {:catch}
          <Avatar size="xs" />{user.name}
          {/await}
        </DropdownItem>
        {/await}
        {/if}
      {/each}
      <DropdownItem on:click={() => navigate("/signin")}>+ Add user</DropdownItem>
    </Dropdown>
    <DropdownItem on:click={signout}>Sign out</DropdownItem>
  </Dropdown>
  {/if}
</Navbar>
<Router>
  <div class="flex">
  {#if $tokens.length}
        <ProjectSwitcher />
  {/if}
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
    <Route path="/settings">
      <Settings bind:logo />
    </Route>
    <Route path="/organization" component={Organization} />
    <Route path="/project" component={ProjectManage} />
    <Route path="/project/:pid" let:params>
      <Project pid={params.pid} />
    </Route>
  </main>
  </div>
</Router>
</div>
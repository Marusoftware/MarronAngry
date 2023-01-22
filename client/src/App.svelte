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
    Chevron
  } from "flowbite-svelte";
  import { Router, Route, navigate } from "svelte-routing";
  import { accessToken, authAPI, destroyNotification, notifications, userAPI } from "./utils";

  import Home from "./pages/Home.svelte";
  import Signin from "./pages/Signin.svelte";
  import Signup from "./pages/Signup.svelte";
  import Notification from "./components/Notification.svelte";
  import { onMount } from "svelte";
  import Settings from "./pages/Settings.svelte";
  import { user } from "./utils/store";
  import type { Token } from "./openapi";
  import Organization from "./pages/Organization.svelte";
  let tokens:Token[]
  onMount(async () => {
    tokens=await authAPI.authSession()
    if(tokens.length!=0 && !$accessToken){
      accessToken.set(tokens[0].accessToken)
    }
  })

  async function signout() {
    await authAPI.authSignout()
    tokens=await authAPI.authSession()
    if(tokens.length!=0 && !$accessToken){
      accessToken.set(tokens[0].accessToken)
    } else {
      accessToken.set("")
    }
  }

  async function changeUser(token:string){
    accessToken.set(token)
  }
</script>

<div class="bg-white dark:bg-gray-800 min-h-screen">
<Navbar let:hidden let:toggle>
  <NavBrand href="/">
    <img src="/marron.jpg" alt="Marron Logo" class="mr-3 h-6 sm:h-9" />
    <span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Marron</span>
  </NavBrand>
  <div class="flex items-center md:order-2">
    {#if $accessToken}
      <Avatar id="avatar-menu" src="/images/profile-picture-3.webp" />
    {:else}
      <Button size="sm" on:click={() => navigate("/signin")} >サインイン</Button>
    {/if}
    <DarkMode />
    <NavHamburger on:click={toggle} class1="w-full md:flex md:w-auto md:order-1"/>
  </div>
  {#if $accessToken}
  <Dropdown placement="bottom" triggeredBy="#avatar-menu">
    <DropdownHeader>
    <span class="block text-sm"> { $user.fullname }</span>
    <span class="block truncate text-sm font-medium"> {$user.email} </span>
    </DropdownHeader>
    <DropdownItem on:click={()=>{navigate("/settings")}}>Settings</DropdownItem>
    <DropdownDivider />
    <DropdownItem class="flex items-center justify-between"><Chevron placement="right">Switch Account</Chevron></DropdownItem>
    <Dropdown placement="left-start">
      {#each tokens as token (token.accessToken)}
        {#await userAPI.userGet({id:token.userId})}
        <DropdownItem>Getting user info...</DropdownItem>
        {:then user}
        <DropdownItem on:click={()=>{changeUser(token.accessToken)}}>
          <Avatar src="/images/profile-picture-3.webp" size="xs" />{user.name}
        </DropdownItem>
        {/await}
      {/each}
      <DropdownItem on:click={() => navigate("/signin")}>+ Add user</DropdownItem>
    </Dropdown>
    <DropdownItem on:click={signout}>Sign out</DropdownItem>
  </Dropdown>
  {/if}
  <NavUl {hidden}>
    <NavLi href="#" on:click={() => navigate("/organization")}>Organization</NavLi>
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
  </main>
</Router>
</div>
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
  } from "flowbite-svelte";
  import { Router, Route, navigate } from "svelte-routing";
  import { destroyNotification, notifications } from "./utils";

  import Home from "./pages/Home.svelte";
  import Signin from "./pages/Signin.svelte";
  import Signup from "./pages/Signup.svelte";
  import Notification from "./components/Notification.svelte";
  import Field from "./components/Field.svelte";

</script>

<div class="bg-white dark:bg-gray-800 min-h-screen">
<Navbar let:hidden let:toggle>
  <NavBrand href="/">
    <img src="/marron.jpg" alt="Marron Logo" class="mr-3 h-6 sm:h-9" />
    <span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">Marron</span>
  </NavBrand>
  <div class="flex items-center md:order-2">
    <!-- <Avatar id="avatar-menu" src="/images/profile-picture-3.webp" /> -->
    <Button size="sm" on:click={() => navigate("/signin")} >サインイン</Button>
    <DarkMode />
    <NavHamburger on:click={toggle} class1="w-full md:flex md:w-auto md:order-1"/>
  </div>
  <Dropdown placement="bottom" triggeredBy="#avatar-menu">
    <DropdownHeader>
    <span class="block text-sm"> Bonnie Green </span>
    <span class="block truncate text-sm font-medium"> name@flowbite.com </span>
    </DropdownHeader>
    <DropdownItem>Dashboard</DropdownItem>
    <DropdownItem>Settings</DropdownItem>
    <DropdownItem>Earnings</DropdownItem>
    <DropdownDivider />
    <DropdownItem>Sign out</DropdownItem>
  </Dropdown>
  <NavUl {hidden}>
    <NavLi href="/" active={true}>Home</NavLi>
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
  </main>
</Router>
</div>
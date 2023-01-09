<script lang="ts">
  import "carbon-components-svelte/css/all.css";
  import {
    Header,
    HeaderNav,
    HeaderNavItem,
    SkipToContent,
    Content,
    Theme,
    SideNav,
    SideNavItems,
    SideNavLink,
    SideNavMenuItem,
    SideNavMenu,
    SideNavDivider,
    HeaderUtilities,
    HeaderGlobalAction
  } from "carbon-components-svelte";
  import { Router, Route, navigate } from "svelte-routing";
  import type { CarbonTheme } from "carbon-components-svelte/types/Theme/Theme.svelte";
  import Fade from "carbon-icons-svelte/lib/Fade.svelte";
  import Asleep from "carbon-icons-svelte/lib/Asleep.svelte";
  import UserAvatarFilledAlt from "carbon-icons-svelte/lib/UserAvatarFilledAlt.svelte";
  let isSideNavOpen = false;
  let theme: CarbonTheme;

  function toggleTheme() {
    if (theme !== "white") {
      theme = "white";
    } else {
      theme = "g80";
    }
  }

  import Home from "./pages/Home.svelte";
  import Signin from "./pages/Signin.svelte";
    import Signup from "./pages/Signup.svelte";
</script>

<Theme bind:theme persist persistKey="__carbon-theme" />

<Router>
  <Header platformName="Marron" bind:isSideNavOpen>
    <svelte:fragment slot="skip-to-content">
      <SkipToContent />
    </svelte:fragment>
    <HeaderNav>
      <HeaderNavItem href="/" text="Link 1" />
    </HeaderNav>
    <HeaderUtilities>
      <HeaderGlobalAction
        aria-label="Settings"
        icon={Asleep}
        on:click={toggleTheme}
      />
      <HeaderGlobalAction icon={UserAvatarFilledAlt} on:click={() => navigate("/signin")} />
    </HeaderUtilities>
  </Header>

  <SideNav bind:isOpen={isSideNavOpen} rail>
    <SideNavItems>
      <SideNavLink icon={Fade} text="Link 1" href="/" isSelected />
      <SideNavLink icon={Fade} text="Link 2" href="/" />
      <SideNavLink icon={Fade} text="Link 3" href="/" />
      <SideNavMenu icon={Fade} text="Menu">
        <SideNavMenuItem href="/" text="Link 1" />
        <SideNavMenuItem href="/" text="Link 2" />
        <SideNavMenuItem href="/" text="Link 3" />
      </SideNavMenu>
      <SideNavDivider />
      <SideNavLink icon={Fade} text="Link 4" href="/" />
    </SideNavItems>
  </SideNav>

  <Content>
    <main>
      <Route path="" component={Home} />
      <Route path="/signin" component={Signin} />
      <Route path="/signup" component={Signup} />
    </main>
  </Content>
</Router>

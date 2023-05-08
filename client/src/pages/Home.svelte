<script type="ts">
    import { Heading } from "flowbite-svelte";
    import { user } from "../utils/store";
    import { SvelteGantt, SvelteGanttTable } from 'svelte-gantt';
    import { onMount } from "svelte";
    onMount(() => {
        const gantt = new SvelteGantt({ target: document.getElementById('gantt')});
    });
</script>
<Heading tag="h1">
    Welcome to Marron{#if $user}
        , {$user.fullname}!
    {/if}
    <div id="gantt"></div>
</Heading>

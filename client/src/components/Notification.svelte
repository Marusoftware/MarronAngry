<script lang="ts">
    let open=true;
    export let title:string
    export let subtitle:string
    export let kind="info"
    import { Toast } from 'flowbite-svelte';
    import { createEventDispatcher } from 'svelte';
    import { ExclamationTriangle, InformationCircle } from "svelte-heros-v2";

	const dispatch = createEventDispatcher();
    function onClose(open:Boolean) {
        if(!open){
            dispatch("close")
        }
    }
    $: onClose(open)
    const kinds={
        info:{ color:"blue", icon:InformationCircle},
        warn:{ color:"yellow", icon:ExclamationTriangle },
    }
</script>

<Toast bind:open color={kinds[kind].color} divClass="w-full max-w-xs p-4 my-2">
    <svelte:fragment slot="icon">
        <svelte:component this={kinds[kind].icon} />
    </svelte:fragment>
    {#if subtitle}
        <span class="font-semibold text-gray-900 dark:text-white">{title}</span>
    {:else}
        {title}
    {/if}
    <div class="mt-3" slot="extra">  
        <div class="mb-2 text-sm font-normal">{subtitle}</div>
        <slot name="actions"></slot>
    </div>
</Toast>
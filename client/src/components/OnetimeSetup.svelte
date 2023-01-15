<script lang="ts">
    import { authAPI } from "../utils";
    import { QRCodeImage } from "svelte-qrcode-image";
    import { Button, Heading, Modal } from "flowbite-svelte";
    import { createEventDispatcher } from "svelte";
    export let open=true;
    const dispatch=createEventDispatcher()
    let value="a"

    async function onOpen() {
        value=(await authAPI.authOtpSetup()).replaceAll('"',"")
    }

    async function submit(){
        open=false
        dispatch("submit")
    }
</script>

<Modal bind:open on:submit={submit} on:open={onOpen} title="One time token">
    <Heading>QRコードを認証アプリで読み取ってください。</Heading>
    <QRCodeImage text={value}/>
    <svelte:fragment slot='footer'>
        <Button on:click={submit}>完了</Button>
        <Button on:click={() => open=false}>キャンセル</Button>
    </svelte:fragment>
</Modal>
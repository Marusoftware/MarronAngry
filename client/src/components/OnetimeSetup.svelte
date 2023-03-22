<script lang="ts">
    import { authAPI } from "../utils";
    import Qrcode from "svelte-qrcode";
    import { Button, Heading, Modal } from "flowbite-svelte";
    import { createEventDispatcher } from "svelte";
    export let open=true;
    export let allowDelete=false;
    const dispatch=createEventDispatcher()
    let value=""
    let otpRecovery=""

    async function onOpen() {
        const otp=await authAPI.authOtpSetup()
        value=otp.otpUrl
        otpRecovery=otp.otpRecovery
    }

    async function submit(){
        open=false
        dispatch("submit")
    }

    async function deleteOTP() {
        await authAPI.authOtpDelete()
        open=false
    }
</script>

<Modal bind:open on:submit={submit} on:open={onOpen} title="One time token">
    <Heading>QRコードを認証アプリで読み取ってください。</Heading>
    <Qrcode value={value}  />
    携帯電話が使用できなくなった場合に備え、以下のリカバリーキーを安全な場所に保管してください:
    {otpRecovery}
    <svelte:fragment slot='footer'>
        <Button on:click={submit}>完了</Button>
        <Button on:click={() => open=false}>キャンセル</Button>
        {#if allowDelete}
            <Button on:click={deleteOTP}>削除</Button>
        {/if}
    </svelte:fragment>
</Modal>
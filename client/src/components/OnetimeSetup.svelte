<script lang="ts">
    import {
        ComposedModal,
        ModalHeader,
        ModalBody,
        ModalFooter,
    } from "carbon-components-svelte"
    import { authAPI } from "../openapi";
    import { QRCodeImage } from "svelte-qrcode-image";
    export let open=true;

    let value="a"

    async function onOpen() {
        value=(await authAPI.authOtpSetup()).replaceAll('"',"")
    }

    async function submit(){
        open=false
    }
</script>

<ComposedModal bind:open on:submit={submit} on:open={onOpen} on:close>
    <ModalHeader label="One time token" title="QRコードを認証アプリで読み取ってください。" />
        <ModalBody>
            <QRCodeImage text={value}/>
        </ModalBody>
    <ModalFooter primaryButtonText="完了" secondaryButtonText="キャンセル" />
</ComposedModal>
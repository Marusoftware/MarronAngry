<script lang="ts">
    import { Button, Heading, Modal } from "flowbite-svelte";
    import { createEventDispatcher } from "svelte";
    import { form, field } from 'svelte-forms';
    import { max, required } from "svelte-forms/validators";
    import { tokens, authAPI } from "../utils";
    import Field from "./Field.svelte";
    export let open=true;
    export let preToken:string
    const dispatch=createEventDispatcher()

    let token=field("token", "", [required(), max(6)])
    const onetimeForm=form(token)

    async function submit(e:Event){
        e.preventDefault()
        await onetimeForm.validate()
        if(!$onetimeForm){
            return
        }
        const token_auth=await authAPI.authOtpAuth({
            preToken: preToken,
            token:$token.value
        })
        tokens.update((v)=>{
            v.splice(0)
            v.unshift(token_auth)
            return v
        })
        open=false;
        dispatch("submit")
    }
</script>

<Modal bind:open title="One time token">
    <Heading>ワンタイムトークンを入力してください。</Heading>
    <Field
        type="password"
        label="One time token"
        placeholder="Enter an One time token..."
        bind:store={token}
    />
    <svelte:fragment slot="footer">
        <Button on:click={submit} disabled={!$onetimeForm.valid}>認証</Button>
    </svelte:fragment>
</Modal>
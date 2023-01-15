<script lang="ts">
    import { Button, Heading, Modal } from "flowbite-svelte";
    import { form, field } from 'svelte-forms';
    import { max, required } from "svelte-forms/validators";
    import { accessToken, authAPI } from "../utils";
    import Field from "./Field.svelte";
    export let open=true;
    export let preToken:string

    const token=field("token", "", [required(), max(6)])
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
        accessToken.set(token_auth.accessToken)
        open=false;
    }
</script>

<Modal bind:open title="One time token">
    <Heading>ワンタイムトークンを入力してください。</Heading>
    <Field
        type="password"
        labelText="One time token"
        placeholder="Enter an One time token..."
        bind:value={$token.value}
        invalid={$token.invalid}
        invalidText={$token.errors.join(", ")}
    />
    <svelte:fragment slot="footer">
        <Button on:click={submit} disabled={!$onetimeForm.valid}>認証</Button>
    </svelte:fragment>
</Modal>
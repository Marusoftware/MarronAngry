<script lang="ts">
    import {
        ComposedModal,
        ModalHeader,
        ModalBody,
        ModalFooter,
        TextInput
    } from "carbon-components-svelte"
    import { form, field } from 'svelte-forms';
    import { max, required } from "svelte-forms/validators";
    import { accessToken, authAPI } from "../utils";
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
    }
</script>

<ComposedModal bind:open on:submit={submit}>
    <ModalHeader label="One time token" title="ワンタイムトークンを入力してください。" />
    <ModalBody hasForm>
        <TextInput
          labelText="One time token"
          placeholder="Enter an One time token..."
          bind:value={$token.value}
          invalid={$token.invalid}
          invalidText={$token.errors.join(", ")}
        />
    </ModalBody>
    <ModalFooter primaryButtonText="Proceed" primaryButtonDisabled={!$onetimeForm.valid} />
</ComposedModal>
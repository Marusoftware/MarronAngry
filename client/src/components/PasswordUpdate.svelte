<script lang="ts">
    import { Button, Heading, Modal } from "flowbite-svelte";
    import { field, form } from "svelte-forms";
    import { matchField, required } from "svelte-forms/validators";
    import { tokens, userAPI } from "../utils";
    import Field from "./Field.svelte";

    const oldpassword = field('oldpassword', '', [required()])
    const password = field('password', '', [required()])
    const passwordConfirmation = field('passwordConfirmation', '', [required(), matchField(password)])
    const updateForm = form(oldpassword, password, passwordConfirmation)

    export let open = false;

    async function submit(e:Event){
        e.preventDefault()
        if($tokens[0].isSso){
            $oldpassword.value="very_strong_password"
            await updateForm.validate()
            if(!$updateForm.valid){
                return
            }
            await userAPI.userUpdateMe({
                userUpdate:{
                    newPassword:$password.value
                }
            })
            $tokens[0].isSso=false
        } else {
            await updateForm.validate()
            if(!$updateForm.valid){
                return
            }
            await userAPI.userUpdateMe({
                userUpdate:{
                    oldPassword:$oldpassword.value,
                    newPassword:$password.value
                }
            })
        }
        
    }

</script>

{#if $tokens[0].isSso}
<Modal bind:open title="パスワードの設定">
    あなたのアカウントは外部のアカウント経由で作成されたため、パスワードが設定されておらず、サインインページでメールアドレスとパスワードを入力してのログインができないようになっています。
    ここでパスワードを設定すると、あなたのアカウントが通常のMarusoftwareアカウントとして利用できるようになります。
    <form on:submit={submit}>
        <Field id="password2" type="password" labelText="New Password" placeholder="Enter password..." bind:value={$password.value} invalid={$password.invalid} invalidText={$password.errors.join(", ")} />
        <Field id="password3" type="password" labelText="New Password Confirmation" placeholder="Enter password again..." bind:value={$passwordConfirmation.value} invalid={$passwordConfirmation.invalid} invalidText={$passwordConfirmation.errors.join(", ")} />
    </form>
    <svelte:fragment slot="footer">
        <Button on:click={submit} disabled={!$updateForm.valid}>設定</Button>
    </svelte:fragment>
</Modal>
{:else}
<Modal bind:open title="パスワードの変更">
    <Heading>現在のパスワードと新しいパスワードを入力してください。</Heading>
    <form on:submit={submit}>
        <Field id="password" type="password" labelText="Old Password" placeholder="Enter old password..." bind:value={$oldpassword.value} invalid={$oldpassword.invalid} invalidText={$oldpassword.errors.join(", ")} />
        <Field id="password2" type="password" labelText="New Password" placeholder="Enter password..." bind:value={$password.value} invalid={$password.invalid} invalidText={$password.errors.join(", ")} />
        <Field id="password3" type="password" labelText="New Password Confirmation" placeholder="Enter password again..." bind:value={$passwordConfirmation.value} invalid={$passwordConfirmation.invalid} invalidText={$passwordConfirmation.errors.join(", ")} />
    </form>
    <svelte:fragment slot="footer">
        <Button on:click={submit} disabled={!$updateForm.valid}>変更</Button>
    </svelte:fragment>
</Modal>
{/if}

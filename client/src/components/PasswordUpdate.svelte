<script lang="ts">
    import { Button, Heading, Modal } from "flowbite-svelte";
    import { field, form } from "svelte-forms";
    import { matchField, required } from "svelte-forms/validators";
    import { tokens, userAPI } from "../utils";
    import Field from "./Field.svelte";

    let oldpassword = field('oldpassword', '', [required()])
    let password = field('password', '', [required()])
    let passwordConfirmation = field('passwordConfirmation', '', [required(), matchField(password)])
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
        <Field type="password" label="New Password" placeholder="Enter password..." bind:store={password} />
        <Field type="password" label="New Password Confirmation" placeholder="Enter password again..." bind:store={passwordConfirmation} />
    </form>
    <svelte:fragment slot="footer">
        <Button on:click={submit} disabled={!$updateForm.valid}>設定</Button>
    </svelte:fragment>
</Modal>
{:else}
<Modal bind:open title="パスワードの変更">
    <Heading>現在のパスワードと新しいパスワードを入力してください。</Heading>
    <form on:submit={submit}>
        <Field type="password" label="Old Password" placeholder="Enter old password..." bind:store={oldpassword} />
        <Field type="password" label="New Password" placeholder="Enter password..." bind:store={password} />
        <Field type="password" label="New Password Confirmation" placeholder="Enter password again..." bind:store={passwordConfirmation} />
    </form>
    <svelte:fragment slot="footer">
        <Button on:click={submit} disabled={!$updateForm.valid}>変更</Button>
    </svelte:fragment>
</Modal>
{/if}

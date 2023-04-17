<script lang="ts">
    import { Button, Heading, Modal } from "flowbite-svelte";
    import { field, form } from "svelte-forms";
    import { required } from "svelte-forms/validators";
    import { tokens, userAPI } from "../utils";
    import Field from "./Field.svelte";

    const password = field('password', '', [required()])
    const updateForm = form(password)
    export let open = false;

    async function submit(e:Event){
        e.preventDefault()
        if(!$tokens[0].isSso){
            await updateForm.validate()
            if(!$updateForm.valid){
                return
            }
            await userAPI.userDeleteMe({
                password:$password.value
            })
        } else {
            await userAPI.userDeleteMe()
        }
        tokens.update((v)=>{
            v.splice(0)
            return v
        })
        open=false
        location.href="/"
    }
</script>

<Modal bind:open title="アカウントの削除">
    {#if $tokens[0].isSso}
    <Heading>本当にアカウントを削除してもよろしいですか?</Heading>
    {:else}
    <Heading>本当にアカウントを削除してもよろしければ、パスワードを入力してください</Heading>
    <form on:submit={submit}>
        <Field id="password" type="password" labelText="Password" placeholder="Enter password..." bind:value={$password.value} invalid={$password.invalid} invalidText={$password.errors.join(", ")} />
    </form>
    {/if}
    <svelte:fragment slot="footer">
        <Button on:click={submit} disabled={!$updateForm.valid}>削除</Button><Button on:click={()=>open=false}>キャンセル</Button>
    </svelte:fragment>
</Modal>
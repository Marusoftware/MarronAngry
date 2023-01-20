<script lang="ts">
    import { Button, Heading, Modal } from "flowbite-svelte";
    import { field, form } from "svelte-forms";
    import { required } from "svelte-forms/validators";
    import { accessToken, userAPI } from "../utils";
    import { user } from "../utils/store";
    import Field from "./Field.svelte";

    const password = field('password', '', [required()])
    const updateForm = form(password)
    export let open = false;

    async function submit(e:Event){
        e.preventDefault()
        await updateForm.validate()
        if(!$updateForm.valid){
            return
        }
        await userAPI.userDeleteMe({
            password:$password.value
        })
        user.set(null)
        accessToken.set("")
        open=false
    }
</script>

<Modal bind:open title="アカウントの削除">
    <Heading>本当にアカウントを削除してもよろしければ、パスワードを入力してください</Heading>
    <form on:submit={submit}>
        <Field id="password" type="password" labelText="Password" placeholder="Enter password..." bind:value={$password.value} invalid={$password.invalid} invalidText={$password.errors.join(", ")} />
    </form>
    <svelte:fragment slot="footer">
        <Button on:click={submit} disabled={!$updateForm.valid}>削除</Button>
    </svelte:fragment>
</Modal>
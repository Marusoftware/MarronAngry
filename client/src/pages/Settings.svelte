<script lang="ts">
    import Field from "../components/Field.svelte";
    import { form, field } from "svelte-forms";
    import { email, max, required } from "svelte-forms/validators";
    import { user } from "../utils/store";
    import { Button, Heading } from "flowbite-svelte";
    import { userAPI } from "../utils";
    import PasswordUpdate from "../components/PasswordUpdate.svelte";
    import OnetimeSetup from "../components/OnetimeSetup.svelte";
    import AccountDelete from "../components/AccountDelete.svelte";

    const name = field("name", $user.name, [required(), max(1024)]);
    const fullname = field("fullname", $user.fullname, [max(1024)]);
    const mail = field("email", $user.email, [required(), email(), max(1024)]);

    const updateForm = form(
        name,
        fullname,
        mail,
    );

    async function submit(e:Event) {
        e.preventDefault()
        await updateForm.validate()
        if(!$updateForm.valid){
            return
        }
        user.set(await userAPI.userUpdateMe({
            userUpdate: {
                name:$name.value,
                fullname:$fullname.value,
                email:$mail.value
            }
        }))
    }
    function reset(e:Event) {
        e.preventDefault()
        updateForm.reset()
    }

    let passwordOpen=false
    let otpOpen=false
    let deleteOpen=false
</script>

<PasswordUpdate bind:open={passwordOpen} />
<OnetimeSetup bind:open={otpOpen} allowDelete />
<AccountDelete bind:open={deleteOpen} />

<Heading>Settings</Heading>
<form on:submit={submit} on:reset={reset}>
    <Field
        id="name"
        labelText="User name"
        placeholder="Enter user name..."
        bind:value={$name.value}
        invalid={$name.invalid}
        invalidText={$name.errors.join(", ")}
    />
    <Field
        id="fullname"
        labelText="User fullname"
        placeholder="Enter user fullname..."
        bind:value={$fullname.value}
        invalid={$fullname.invalid}
        invalidText={$fullname.errors.join(", ")}
    />
    <Field
        id="email"
        type="email"
        labelText="Email address"
        placeholder="Enter email address..."
        bind:value={$mail.value}
        invalid={$mail.invalid}
        invalidText={$mail.errors.join(", ")}
    />
    <Button type="submit">更新</Button> <Button type="reset">リセット</Button>
</form>
<Button on:click={()=>{passwordOpen=true}}>パスワードの変更</Button> <Button on:click={()=>{otpOpen=true}}>ワンタイムトークンの設定</Button> <Button on:click={()=>{deleteOpen=true}}>アカウントの削除</Button>
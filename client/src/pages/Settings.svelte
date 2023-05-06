<script lang="ts">
    import Field from "../components/Field.svelte";
    import { form, field } from "svelte-forms";
    import { email, max, required } from "svelte-forms/validators";
    import { Button, Fileupload, Heading, Helper, Label } from "flowbite-svelte";
    import { tokens, userAPI } from "../utils";
    import PasswordUpdate from "../components/PasswordUpdate.svelte";
    import OnetimeSetup from "../components/OnetimeSetup.svelte";
    import AccountDelete from "../components/AccountDelete.svelte";
    import { user } from "../utils/store";

    export let logo: string | ArrayBuffer
    let logo_file:FileList;
    let name = field("name", $user.name, [required(), max(1024)]);
    let fullname = field("fullname", $user.fullname, [max(1024)]);
    let mail = field("email", $user.email, [required(), email(), max(1024)]);

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

    async function updateLogo(e) {
        await userAPI.userSetLogo({image:e.target.files[0]})
        logo=URL.createObjectURL(e.target.files[0]);
    }

    let passwordOpen=false
    let otpOpen=false
    let deleteOpen=false
</script>

<PasswordUpdate bind:open={passwordOpen} />
<OnetimeSetup bind:open={otpOpen} allowDelete />
<AccountDelete bind:open={deleteOpen} />

<Heading>Settings</Heading>
<Label for="logo" class="pb-2">Upload logo</Label>
<Fileupload id="logo" bind:files={logo_file} on:change={updateLogo} style="display:none" ></Fileupload>
<Helper>PNG or JPG</Helper>
<form on:submit={submit} on:reset={reset}>
    <Field
        label="User name"
        placeholder="Enter user name..."
        bind:store={name}
        invalid={$name.invalid}
        invalidText={$name.errors.join(", ")}
    />
    <Field
        label="User fullname"
        placeholder="Enter user fullname..."
        bind:store={fullname}
    />
    <Field
        type="email"
        label="Email address"
        placeholder="Enter email address..."
        bind:store={mail}
    />
    <div class="space-x-1"><Button type="submit">更新</Button><Button type="reset">リセット</Button></div>
</form>
<div class="py-1 space-x-1">
<Button on:click={()=>{passwordOpen=true}}>{#if $tokens[0].isSso}パスワードの設定(Marusoftwareアカウントへの移行){:else}パスワードの変更{/if}</Button>
{#if !$tokens[0].isSso}<Button on:click={()=>{otpOpen=true}}>ワンタイムトークンの設定</Button>{/if}
<Button on:click={()=>{deleteOpen=true}}>アカウントの削除</Button>
</div>

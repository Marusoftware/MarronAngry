<script lang="ts">
  import Google from "svelte-material-icons/Google.svelte";
  
  import { form, field } from 'svelte-forms';
  import { max, required } from 'svelte-forms/validators';
  import { authAPI, accessToken } from "../utils";
  import Onetime from "../components/Onetime.svelte";
  import { navigate } from "svelte-routing";
  import { A, Button, Card, Heading, Popover } from "flowbite-svelte";
  import Field from "../components/Field.svelte";

  export let username=""
  const name = field('name', username, [required(), max(1024)])
  const password = field('password', '', [required(), max(1024)])
  const loginForm = form(name, password)
  let OnetimeOpen=false
  let preToken=""

  async function submit(e:Event) {
    e.preventDefault()
    await loginForm.validate()
    if(!$loginForm.valid){
      return
    }
    const token=await authAPI.authSignin({
      username:$name.value,
      password:$password.value
    })
    if(token.tokenType=="bearer"){
      accessToken.set(token.accessToken)
    } else {
      preToken=token.accessToken
      OnetimeOpen=true
    }
  }
</script>

<Onetime bind:open={OnetimeOpen} bind:preToken />

<div class="grid grid-cols-2">
  <div class="col-span-1">
    <Heading>初めての方と<br />他のサービスでのログインをされる方</Heading>
    <Button on:click={() => navigate("/signup")} >Marusoftwareアカウントを作成</Button>
    <Card>
      <Button id="google" class="m-auto" href="/api/v1/auth/sso/google"><Google /></Button>
      <Popover triggeredBy="#google">Signin/Signup with Google</Popover>
    </Card>
  </div>
  <div class="col-span-1">
    <Heading>Marusoftwareアカウントをお持ちの方</Heading>
    <form on:submit={submit}>
    <Field 
      id="name"
      labelText="User name or Email"
      placeholder="Enter user name or email..."
      bind:value={$name.value}
      invalid={$name.invalid}
      invalidText={$name.errors.join(", ")}
    />
    <Field id="password" type="password" labelText="Password" placeholder="Enter password..." bind:value={$password.value} invalid={$password.invalid} invalidText={$password.errors.join(", ")} />
    サインインすると、
    <A inline href="https://marusoftware.net/privacypolicy.html">
      プライバシーポリシー
    </A>に同意したこととなります。予めご確認ください。<br />
    <Button type="submit" disabled={!$loginForm.valid}  >サインイン</Button>
    </form>
  </div>
</div>

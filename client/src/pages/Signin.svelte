<script lang="ts">
  import {
    Grid,
    Row,
    Column,
    Form,
    Button,
    PasswordInput,
    TextInput,
    Tile,
    Link,
  } from "carbon-components-svelte";
  import Google from "svelte-material-icons/Google.svelte";
  
  import { form, field } from 'svelte-forms';
  import { required } from 'svelte-forms/validators';
  import { authAPI, userAPI, accessToken } from "../openapi";

  const name = field('name', '', [required()])
  const password = field('password', '', [required()])
  const loginForm = form(name, password)

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
    accessToken.set(token.accessToken)
  }
</script>

<Grid>
  <Row>
    <Column>
      <h1>初めての方と<br />他のサービスでのログインをされる方</h1>
      <Button>Marusoftwareアカウントを作成</Button>
      <Tile>
        <Button icon={Google} iconDescription="Signin/Signup with Google" href="/api/v1/auth/sso/google" />
      </Tile>
    </Column>
    <Column>
      <h1>Marusoftwareアカウントをお持ちの方</h1>
      <Form on:submit={submit}>
        <TextInput
          labelText="User name or Email"
          placeholder="Enter user name or email..."
          bind:value={$name.value}
          invalid={$name.invalid}
          invalidText={$name.errors.join(", ")}
        />
        <PasswordInput labelText="Password" placeholder="Enter password..." bind:value={$password.value} invalid={$password.invalid} invalidText={$password.errors.join(", ")} />
        サインインすると、
        <Link inline href="https://marusoftware.net/privacypolicy.html">
          プライバシーポリシー
        </Link>に同意したこととなります。予めご確認ください。<br />
        <Button type="submit" disabled={!$loginForm.valid} >サインイン</Button>
      </Form>
    </Column>
  </Row>
</Grid>

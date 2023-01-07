<script type="ts">
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
</script>

<Grid>
  <Row>
    <Column>
      <h1>初めての方と<br />他のサービスでのログインをされる方</h1>
      <Button>Marusoftwareアカウントを作成</Button>
      <Tile>
        <Button icon={Google} iconDescription="Signin/Signup with Google" />
      </Tile>
    </Column>
    <Column>
      <h1>Marusoftwareアカウントをお持ちの方</h1>
      <Form on:submit>
        <TextInput
          labelText="User name or Email"
          placeholder="Enter user name or email..."
        />
        <PasswordInput labelText="Password" placeholder="Enter password..." />
        サインインすると、
        <Link inline href="https://marusoftware.net/privacypolicy.html">
          プライバシーポリシー
        </Link>に同意したこととなります。予めご確認ください。<br />
        <Button type="submit">Submit</Button>
      </Form>
    </Column>
  </Row>
</Grid>

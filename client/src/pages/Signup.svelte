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
    ProgressIndicator,
    ProgressStep,
    OrderedList,
    ListItem
  } from "carbon-components-svelte";
  
  import { form, field } from 'svelte-forms';
  import { email, matchField, required } from 'svelte-forms/validators';
  import { authAPI, userAPI, accessToken, type User } from "../openapi";
  import { navigate } from "svelte-routing";
  import OnetimeSetup from "../components/OnetimeSetup.svelte";

  const name = field('name', '', [required()])
  const fullname = field('fullname', '', [])
  const mail = field('email', '', [required(), email()])
  const password = field('password', '', [required()])
  const passwordConfirmation = field('passwordConfirmation', '', [matchField(password)])
  const loginForm = form(name, fullname, mail, password, passwordConfirmation)

  let currentIndex=0
  let user:User
  async function submit(e:Event) {
    e.preventDefault()
    await loginForm.validate()
    if(!$loginForm.valid){
      return
    }
    user=await authAPI.authSignup({
      userCreate:{
        name:$name.value,
        fullname:$fullname.value,
        email:$mail.value,
        password:$password.value
      }
    })
    currentIndex=2
  }
  let oneTimeOpen=false;
  async function goOneTime(){
    const token=await authAPI.authSignin({
      username:user.name,
      password:$password.value
    })
    accessToken.set(token.accessToken)
    oneTimeOpen=true
  }
</script>

<Grid>
  <ProgressIndicator spaceEqually bind:currentIndex preventChangeOnClick>
    <ProgressStep 
      label="プライバシーポリシー"
      description="サービスの利用にはプライバシーポリシーへの同意が必要です。"
    />
    <ProgressStep 
      label="アカウント作成"
      description="必要な情報を入力して、アカウントを作成します。"
    />
    <ProgressStep 
      label="追加のセキュリティ"
      description="「万一」のときにより安全にするために..."
    />
  </ProgressIndicator>
  {#if currentIndex==0}
    <h1>プライバシーポリシーをお読みください。</h1>
    <Row>
      <Column>
    <Tile>
      <OrderedList>
        <ListItem>概要</ListItem>
        この文書はMarusoftwareの全ソフトウェア(ホームページを含む)に対して適用される利用者情報の取り扱い方針です。
        <ListItem>個人情報の取扱について</ListItem>
        Marusoftwareの全ソフトウェアの利用者(以下、利用者とする)がMarusoftwareに対して送信した個人情報に関わるすべてのデータは最大の尊重をいたします。<br />
        従って、その個人情報を利用者の許可無く外部に公開することはありません。<br />
        また、ウェブサイト上または何らかの形で周知された利用方法以外について利用することはございません。<br />
        ただし、以下に示す"セキュリティー上の例外"や、サーバーに対しての不正アクセスなどにより、個人情報が漏洩する可能性が考えられます。<br />
        もちろん、そのようなことのないように管理に当たっていますが、残念ながら"絶対"は存在しません。<br />
        万一漏洩した際には、その情報(漏洩に関する詳細)を速やかに公開いたします。<br />
        ただし、漏洩によって発生したいかなる損害に対してもMarusoftwareは責任をとらないものとします。<br />
        <ListItem>セキュリティ上の例外</ListItem>
        <OrderedList nested>
          <ListItem>利用者の環境が、SSL(TLS)に対応していない。もしくは使用していない。</ListItem> 
          Marusoftwareのサーバーでは2020年11月現在、多くの情報の送受信にTLSによる暗号化を適用できます。<br />
          これを利用することで、この利用者の利用するコンピュータとMarusoftwareのサーバ間で暗号化通信が確立され、利用者の個人情報の不正取得が困難となります。<br />
          <ListItem>Marusoftwareの予期せぬ方法でデータを送信した場合</ListItem>
          Marusoftwareのソフトウェア以外からのデータ送受信や、本来の用途以外での使用を行うと、セキュリティ的に脆弱になることがあります。
          <ListItem>それ以外の理由</ListItem>
        </OrderedList>
        <ListItem>この文章の変更</ListItem>
        この文書は利用者に許可なく変更されることがございます。<br />
        可能な限り多くの利用者にお伝えできるよう努めますが、伝達されなかった場合のいかなる損害も責任はすべて利用者に有するものとします。<br />
        また、変更が伝達されなかった場合でも、常に最新の文書(当プライバシーポリシー)が適用されるものとします。
        <ListItem>変更記録</ListItem>
        ここにこれまでのこの文章の変更を記します。
        <OrderedList nested>
          <ListItem>2019/11/16 作成</ListItem>
          <ListItem>2020/11/16 更新</ListItem>
          <ListItem>2021/12/09 更新</ListItem>
          <ListItem>2022/12/11 更新</ListItem>
        </OrderedList>
        </OrderedList>
    </Tile>
    同意されない場合はこのページを閉じてください。<br />
    <Button on:click={() => {currentIndex=1}}>同意して続行</Button>
    </Column>
    </Row>
  {:else if currentIndex==1}
    <h1>アカウント情報を入力してください</h1>
    <Row>
      <Column>
      <h2>情報が必要な理由</h2>
      <Tile>
        ユーザー名とメールアドレス、パスワードはアカウントへのログイン時に使用します。<br />
        メールアドレスは、ご利用者様へのご連絡に使用する場合もあります。<br />
        パスワードはなるべく推測されにくく多様な種類の文字を用いた長いものにしてください。<br />
        また、タイプミスによるサインイン不能を防止するため、パスワードは2回入力してください。<br />
        フルネームの入力は任意で、他のユーザーには表示されません。<br />
      </Tile>
      </Column>
    <Column>
      <Form on:submit={submit}>
        
        <TextInput
          labelText="User name"
          placeholder="Enter user name..."
          bind:value={$name.value}
          invalid={$name.invalid}
          invalidText={$name.errors.join(", ")}
        />
        <TextInput
          labelText="User fullname"
          placeholder="Enter user fullname..."
          bind:value={$fullname.value}
          invalid={$fullname.invalid}
          invalidText={$fullname.errors.join(", ")}
        />
        <TextInput
          labelText="Email address"
          placeholder="Enter email address..."
          bind:value={$mail.value}
          invalid={$mail.invalid}
          invalidText={$mail.errors.join(", ")}
        />
        <PasswordInput labelText="Password" placeholder="Enter password..." bind:value={$password.value} invalid={$password.invalid} invalidText={$password.errors.join(", ")} />
        <PasswordInput labelText="Password Confirmation" placeholder="Enter password again..." bind:value={$passwordConfirmation.value} invalid={$passwordConfirmation.invalid} invalidText={$passwordConfirmation.errors.join(", ")} />
        <Button type="submit" disabled={!$loginForm.valid} >サインアップ</Button>
      </Form>
    </Column>
    </Row>
  {:else if currentIndex==2}
    <h1>ご苦労さまでした。</h1>
    <h2>最低限必要な登録手続きは終了しました。ワンタイムパスワードを用いた追加のセキュリティはいかがですか?</h2>
    <Button on:click={goOneTime}>利用します。</Button>
    <Button on:click={()=>{navigate(`/signin/${user.name}`)}}>結構です。</Button>
    <OnetimeSetup bind:open={oneTimeOpen}/>
  {/if}
</Grid>

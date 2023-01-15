<script lang="ts">
  import { form, field } from 'svelte-forms';
  import { email, matchField, max, required } from 'svelte-forms/validators';
  import { authAPI, accessToken } from "../utils";
  import { navigate } from "svelte-routing";
  import OnetimeSetup from "../components/OnetimeSetup.svelte";
  import type { User } from "../openapi";
  import { Heading, Button, List, Li, Progressbar, Card } from "flowbite-svelte";
  import Field from "../components/Field.svelte";

  const name = field('name', '', [required(), max(1024)])
  const fullname = field('fullname', '', [max(1024)])
  const mail = field('email', '', [required(), email(), max(1024)])
  const password = field('password', '', [required()])
  const passwordConfirmation = field('passwordConfirmation', '', [required(), matchField(password)])
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

<ol class="items-center w-full space-y-4 sm:flex sm:space-x-8 sm:space-y-0">
  <li class="flex items-center text-blue-500 dark:text-gray-400 space-x-2.5">
      <span class="flex items-center justify-center w-8 h-8 border border-gray-500 rounded-full shrink-0 dark:border-gray-400">
          1
      </span>
      <span>
          <h3 class="font-medium leading-tight">プライバシーポリシー</h3>
          <p class="text-sm">サービスの利用にはプライバシーポリシーへの同意が必要です。<p>
      </span>
    </li>
  <li class="flex items-center text-gray-500 dark:text-gray-400 space-x-2.5">
      <span class="flex items-center justify-center w-8 h-8 border border-gray-500 rounded-full shrink-0 dark:border-gray-400">
          2
      </span>
      <span>
          <h3 class="font-medium leading-tight">アカウント作成</h3>
          <p class="text-sm">必要な情報を入力して、アカウントを作成します。<p>
      </span>
    </li>
  <li class="flex items-center text-gray-500 dark:text-gray-400 space-x-2.5">
      <span class="flex items-center justify-center w-8 h-8 border border-gray-500 rounded-full shrink-0 dark:border-gray-400">
          3
      </span>
      <span>
          <h3 class="font-medium leading-tight">追加のセキュリティ</h3>
          <p class="text-sm">「万一」のときにより安全にするために...<p>
      </span>
  </li>
</ol>
<Progressbar progress={String(Math.round((currentIndex+1)/3*100))} size="h-4" labelInside />
  {#if currentIndex==0}
    <Heading>プライバシーポリシーをお読みください。</Heading>
    <List tag="ol" list="decimal">
      <Li>概要</Li>
      この文書はMarusoftwareの全ソフトウェア(ホームページを含む)に対して適用される利用者情報の取り扱い方針です。
      <Li>個人情報の取扱について</Li>
      Marusoftwareの全ソフトウェアの利用者(以下、利用者とする)がMarusoftwareに対して送信した個人情報に関わるすべてのデータは最大の尊重をいたします。<br />
      従って、その個人情報を利用者の許可無く外部に公開することはありません。<br />
      また、ウェブサイト上または何らかの形で周知された利用方法以外について利用することはございません。<br />
      ただし、以下に示す"セキュリティー上の例外"や、サーバーに対しての不正アクセスなどにより、個人情報が漏洩する可能性が考えられます。<br />
      もちろん、そのようなことのないように管理に当たっていますが、残念ながら"絶対"は存在しません。<br />
      万一漏洩した際には、その情報(漏洩に関する詳細)を速やかに公開いたします。<br />
      ただし、漏洩によって発生したいかなる損害に対してもMarusoftwareは責任をとらないものとします。<br />
      <Li>セキュリティ上の例外</Li>
      <List tag="ul" class="pl-5 mt-2 space-y-1">
       <Li>利用者の環境が、SSL(TLS)に対応していない。もしくは使用していない。</Li> 
       Marusoftwareのサーバーでは2020年11月現在、多くの情報の送受信にTLSによる暗号化を適用できます。<br />
       これを利用することで、この利用者の利用するコンピュータとMarusoftwareのサーバ間で暗号化通信が確立され、利用者の個人情報の不正取得が困難となります。<br />
       <Li>Marusoftwareの予期せぬ方法でデータを送信した場合</Li>
       Marusoftwareのソフトウェア以外からのデータ送受信や、本来の用途以外での使用を行うと、セキュリティ的に脆弱になることがあります。
       <Li>それ以外の理由</Li>
      </List>
      <Li>この文章の変更</Li>
      この文書は利用者に許可なく変更されることがございます。<br />
      可能な限り多くの利用者にお伝えできるよう努めますが、伝達されなかった場合のいかなる損害も責任はすべて利用者に有するものとします。<br />
      また、変更が伝達されなかった場合でも、常に最新の文書(当プライバシーポリシー)が適用されるものとします。
      <Li>変更記録</Li>
      ここにこれまでのこの文章の変更を記します。
      <List tag="ul" class="pl-5 mt-2 space-y-1">
       <Li>2019/11/16 作成</Li>
       <Li>2020/11/16 更新</Li>
       <Li>2021/12/09 更新</Li>
       <Li>2022/12/11 更新</Li>
      </List>
     </List>
    同意されない場合はこのページを閉じてください。<br />
    <Button on:click={() => {currentIndex=1}}>同意して続行</Button>
  {:else if currentIndex==1}
    <Heading>アカウント情報を入力してください</Heading>
    <div class="grid grid-cols-2">
      <div class="col-span-1">
      <Heading tag="h2">情報が必要な理由</Heading>
      <Card horizontal>
        ユーザー名とメールアドレス、パスワードはアカウントへのログイン時に使用します。<br />
        メールアドレスは、ご利用者様へのご連絡に使用する場合もあります。<br />
        パスワードはなるべく推測されにくく多様な種類の文字を用いた長いものにしてください。<br />
        また、タイプミスによるサインイン不能を防止するため、パスワードは2回入力してください。<br />
        フルネームの入力は任意で、他のユーザーには表示されません。<br />
      </Card>
      </div>
      <div class="col-span-1">
      <form on:submit={submit}>
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
        <Field id="password" type="password" labelText="Password" placeholder="Enter password..." bind:value={$password.value} invalid={$password.invalid} invalidText={$password.errors.join(", ")} />
        <Field id="password2" type="password" labelText="Password Confirmation" placeholder="Enter password again..." bind:value={$passwordConfirmation.value} invalid={$passwordConfirmation.invalid} invalidText={$passwordConfirmation.errors.join(", ")} />
        <Button type="submit" disabled={!$loginForm.valid} >サインアップ</Button>
      </form>
    </div>
    </div>
  {:else if currentIndex==2}
    <Heading>ご苦労さまでした。</Heading>
    <Heading tag="h2">最低限必要な登録手続きは終了しました。ワンタイムパスワードを用いた追加のセキュリティはいかがですか?</Heading>
    <Button on:click={goOneTime}>利用します。</Button>
    <Button on:click={()=>{navigate(`/signin/${user.name}`)}}>結構です。</Button>
    <OnetimeSetup bind:open={oneTimeOpen} on:submit={() => {navigate(`/signin/${user.name}`)}} />
  {/if}

<script type="ts">
    import { Heading } from "flowbite-svelte";
    import { user } from "../utils/store";
</script>
<Heading tag="h1">
    Welcome to Marron, {$user.fullname}!
</Heading>

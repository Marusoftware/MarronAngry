<script lang="ts">
	import classNames from 'classnames';
</script>

<button {...$$restProps} class={classNames('flex items-center', $$props.class)} on:click>
	<slot />
</button>
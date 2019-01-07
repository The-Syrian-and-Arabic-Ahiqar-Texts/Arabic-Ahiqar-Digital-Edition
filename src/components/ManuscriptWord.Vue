<template>
  <span v-on:mouseenter="mouseOver" :style="{background: $route.params.parallelGroupID === word.parallelGroupId ? 'lightblue' : 'none'}">
    {{word.surface}}
  </span>
</template>

<script>

export default {
  props: {
    word: {}
  },
  data () {
    return {
    }
  },
  methods: {
    mouseOver () {
      this.$router.push({
        name: 'SPA',
        params: {
          manuscriptID: this.$route.params.manuscriptID,
          pageID: this.$route.params.pageID,
          parallelGroupID: this.word.parallelGroupId
        }
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
span {
  border-radius: 5px;
}
</style>

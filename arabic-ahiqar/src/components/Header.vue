<template>
  <div>
    <span id="title"> حيقار</span><span id="title-english">Digital Online Edition of Arabic Ahiqar</span>
  </div>
</template>

<script>

export default {
  props: {
  },
  data () {
    return {
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div {
  width: 100%;
  display: flex;
  align-items: stretch;
}
#title-english {
  flex-grow: 1;
  font-size: x-large;
  background: tan;
  border-left-style: solid;
}
#title {
  width: 70px;
  font-size: xx-large;
  background: white;
}
</style>

<template>
  <div id="spa">
    <Header id="ahiqar-header"/>
    <Menu id="ahiqar-menu"/>
    <manuscript id="ahiqar-manuscript"/>
    <open-seadragon id="ahiqar-open-seadragon"/>
    <instant-variants id="ahiqar-instant-variants"/>
  </div>
</template>

<script>
import Header from '@/components/Header'
import Menu from '@/components/Menu'
import Manuscript from '@/components/Manuscript'
import InstantVariants from '@/components/InstantVariants'
import OpenSeadragon from '@/components/OpenSeadragon'

export default {
  components: {
    Header,
    Menu,
    manuscript: Manuscript,
    'instant-variants': InstantVariants,
    'open-seadragon': OpenSeadragon
  }
}
</script>

<style scoped>
#spa {
  width: 98vw;
  height: 96vh;
}
#ahiqar-header {
  width: 98vw;
  height: 40px;
}
#ahiqar-menu {
  width: 98vw;
  height: 40px;
  background: lightyellow;
}
#ahiqar-manuscript {
  width: 30%;
  height: calc(96vh - 200px);
  max-height: calc(96vh - 200px);
  background: lightyellow;
  float: right;
  text-align: justify;
}
#ahiqar-open-seadragon {
  width: 70%;
  height: calc(96vh - 200px);
  max-height: calc(96vh - 200px);
  float: left;
  /* margin-right: 10px; */
  background: lightblue;
}
#ahiqar-instant-variants{
  position: absolute;
  top: calc(96vh - 200px + 88px);
  left: 8px;
  width: 98vw;
  height: 130px;
  background: tan;
  overflow: auto;
  text-align: justify;
}
</style>

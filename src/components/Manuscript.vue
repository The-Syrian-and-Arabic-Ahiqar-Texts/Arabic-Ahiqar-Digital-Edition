<template>
  <div>
    <h1>{{manuscriptName}}, page {{pageName}}</h1>
    <div class="text-view">
      <div
        v-if="lines.length > 0"
        v-for="line in lines"
        v-bind:key="line.lineID"
        dir="rtl">
        <span>{{line.lineName}}: </span><manuscript-word v-for="word in line.wordsByLineId.nodes" :word="word"/>
      </div>
    </div>
  </div>
</template>

<script>
import ManuscriptWord from '@/components/ManuscriptWord'

export default {
  props: {
  },
  components: {
    "manuscript-word": ManuscriptWord
  },
  data () {
    return {
      lines: [],
      manuscriptName: '',
      pageName: ''
    }
  },
  watch: {
    $route (to, from) {
      if (to.params !== from.params) {
        this.$graphql.request(`
{
  pageByPageId(pageId:${to.params.pageID}){
    colsByPageId {
      nodes {
        linesByColId {
          nodes {
            lineName
            wordsByLineId {
              nodes {
                surface
                positionInDocument
                parallelGroupId

              }
            }
          }
        }
      }
    }
  }
}
        `)
          .then(res => {
            this.lines = res.pageByPageId.colsByPageId.nodes[0].linesByColId.nodes
          })
          .catch(err => {
            console.log('Error.', err)
          })
        this.$graphql.request(`
{
  pageByPageId(pageId:${to.params.pageID}) {
    pageName
    manuscriptByManuscriptId{
      manuscriptName
    }
  }
}
        `)
          .then(res => {
            this.pageName = res.pageByPageId.pageName
            this.manuscriptName = res.pageByPageId.manuscriptByManuscriptId.manuscriptName
          })
          .catch(err => {
            console.log('Error.', err)
          })
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  max-height: 26px;
  font-size: larger;
  margin-top: 0px;
  margin-bottom: 0px;
  background: tan;
}
.text-view{
  max-height: calc(100% - 26px);
  overflow-y: auto;
}
</style>

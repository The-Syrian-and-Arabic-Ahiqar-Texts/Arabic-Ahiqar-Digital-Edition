<template>
  <div>
    <div v-show="loading"><span>Loading...</span></div>
    <div dir="rtl" v-show="!loading" v-for="variant in apparatus">
      <div>
      <span>{{variant.manuscriptName}}:</span>
      <span v-for="originalWord in variant.original">
        {{originalWord}}
      </span>
      </div>
      <div v-for="alternative in variant.readings">
        <span>{{alternative.manuscriptName}}:</span>
        <span v-for="alternativeWord in alternative.variantReading">
        {{alternativeWord}}
      </span>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  props: {

  },
  data () {
    return {
      loading: false,
      apparatus: []
    }
  },
  watch: {
    $route (to, from) {
      if (to.params.parallelGroupID !== '~' && to.params !== from.params) {
        this.loading = true
        this.$graphql.request(`
{
  parallelGroupByParallelGroupId(parallelGroupId: ${to.params.parallelGroupID}) {
    wordsByParallelGroupId {
      nodes {
        surface
        lineByLineId{
          colByColId {
            pageByPageId {
              manuscriptByManuscriptId{
                manuscriptName
              }
            }
          }
        }
      }
    }
    parallelGroupToParallelGroupsByParallelGroupId1 {
      nodes {
        parallelGroupByParallelGroupId2 {
          wordsByParallelGroupId {
            nodes {
              surface
              lineByLineId{
                colByColId {
                  pageByPageId {
                    manuscriptByManuscriptId{
                      manuscriptName
                    }
                  }
                }
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
            let words = []
            res.parallelGroupByParallelGroupId.wordsByParallelGroupId.nodes.forEach(word => {
              words.push(word.surface)
            })
            const variant = {
              manuscriptName: res.parallelGroupByParallelGroupId.wordsByParallelGroupId.nodes[0].lineByLineId.colByColId.pageByPageId.manuscriptByManuscriptId.manuscriptName,
              original: words
            }
            let readings = []

            res.parallelGroupByParallelGroupId.parallelGroupToParallelGroupsByParallelGroupId1.nodes.forEach(group => {
              if (group.parallelGroupByParallelGroupId2.wordsByParallelGroupId.nodes.length > 0) {
                let reading = {
                  manuscriptName: group.parallelGroupByParallelGroupId2.wordsByParallelGroupId.nodes[0].lineByLineId.colByColId.pageByPageId.manuscriptByManuscriptId.manuscriptName,
                  variantReading: []
                }
                group.parallelGroupByParallelGroupId2.wordsByParallelGroupId.nodes.forEach(word => {
                  reading.variantReading.push(word.surface)
                })
                readings.push(reading)
              }
            })
            variant.readings = readings
            this.loading = false
            this.apparatus = [variant]
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
</style>

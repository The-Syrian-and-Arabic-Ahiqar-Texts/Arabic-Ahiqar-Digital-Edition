<template>
  <div>
    <span v-if="manuscripts.length === 0">Loading...</span>
    <select v-if="manuscripts.length > 0" v-model="selectedManuscript">
        <option
            v-for="manuscript in manuscripts"
            v-bind:value="manuscript"
            v-bind:key="manuscript.manuscriptName">
            {{ manuscript.manuscriptName }}
        </option>
    </select>
    <!-- <span v-if="selectedManuscript">Selected Ms: {{ selectedManuscript.manuscriptName }}</span> -->
    <select v-if="selectedManuscript" v-model="selectedPage">
        <option
            v-for="page in selectedManuscript.pagesByManuscriptId.nodes"
            v-bind:value="page"
            v-bind:key="`${selectedManuscript.manuscriptName}-${page.pageId}`">
            {{ page.pageName }}
        </option>
    </select>
    <!-- <span v-if="selectedPage">Selected Page: {{ selectedPage.pageName }}</span> -->
  </div>
</template>

<script>

export default {
  name: 'Menu',
  props: {
  },
  data () {
    return {
      manuscripts: [],
      selectedManuscript: undefined,
      selectedPage: undefined
    }
  },
  mounted () {
    this.$graphql.request(`
{
  allManuscripts {
    nodes {
      manuscriptName
      manuscriptId
      pagesByManuscriptId {
        nodes {
          pageName
          pageId
        }
      }
    }
  }
}
    `)
      .then(res => {
        this.manuscripts = res.allManuscripts.nodes
        this.selectedManuscript = this.manuscripts[0]
        this.selectedPage = this.selectedManuscript.pagesByManuscriptId.nodes[0]
      })
      .catch(err => {
        console.log('Error.', err)
      })
  },
  apollo: {
    // word: gql('{wordByWordAddress(wordAddress: "Cod. Sach. 339-1-1-3") {surface}}')
  },
  watch: {
    selectedManuscript (newVal, oldVal) {
      if (newVal !== oldVal) {
        this.selectedPage = newVal.pagesByManuscriptId.nodes[0]
      }
    },
    selectedPage (newVal, oldVal) {
      if (newVal !== oldVal) {
        this.$router.push({
          name: 'SPA',
          params: {
            manuscriptID: this.selectedManuscript.manuscriptId,
            pageID: this.selectedPage.pageId,
            parallelGroupID: '~'
          }
        })
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

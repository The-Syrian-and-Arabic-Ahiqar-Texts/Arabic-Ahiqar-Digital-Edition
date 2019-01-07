<template>
    <div :id="id" class="open-sea-dragon"></div>
</template>

<script>
import OpenSeadragon from 'openseadragon'

export default {
  props: {
    id: {
      type: String,
      default: 'openseadragon-viewer'
    },
    prefixUrl: {
      type: String,
      default: '/node_modules/openseadragon/build/openseadragon/images/'
    },
    zoom: '',
    maxZoomLevel: {
      type: Number
    },
    ajaxWithCredentials: {
      type: Boolean
    },
    showNavigator: {
      type: Boolean
    },
    homeFillsViewer: {
      type: Boolean
    },
    navigatorId: {
      type: String
    },
    toolbar: {
      type: String
    },
    zoomInButton: {
      type: String
    },
    zoomOutButton: {
      type: String
    },
    homeButton: {
      type: String
    },
    fullPageButton: {
      type: String
    },
    panHorizontal: {
      type: Boolean,
      default: true
    },
    panVertical: {
      type: Boolean,
      default: true
    },
    mouseNavEnabled: {
      type: Boolean,
      default: true
    }
  },
  components: {
  },
  data () {
    return {
      tileSources: '',
      viewer: undefined
    }
  },
  computed: {
    seaDragonSettings () {
      return {
        id: this.id,
        tileSources: this.tileSources,
        prefixUrl: this.prefixUrl,
        ajaxWithCredentials: this.ajaxWithCredentials,
        showNavigator: this.showNavigator,
        homeFillsViewer: this.homeFillsViewer,
        panHorizontal: this.panHorizontal,
        panVertical: this.panVertical,
        mouseNavEnabled: this.mouseNavEnabled,
        ...this.maxZoomLevel && {maxZoomLevel: this.maxZoomLevel},
        ...this.navigatorId && {navigatorId: this.navigatorId},
        ...this.toolbar && {toolbar: this.toolbar},
        ...this.zoomInButton && {zoomInButton: this.zoomInButton},
        ...this.zoomOutButton && {zoomOutButton: this.zoomOutButton},
        ...this.homeButton && {homeButton: this.homeButton},
        ...this.fullPageButton && {fullPageButton: this.fullPageButton},
        showZoomControl: false,
        showHomeControl: false,
        showFullPageControl: false
      }
    }
  },
  mounted () {
    this.viewer = OpenSeadragon(this.seaDragonSettings)
  },
  watch: {
    zoom (newVal, oldVal) {
      this.viewer.viewport.zoomTo(newVal)
    },
    $route (to, from) {
      if (to.params.pageID !== '~' && to.params.pageID !== from.params.pageID) {
        this.$graphql.request(`
{
  pageByPageId(pageId:${to.params.pageID}) {
    filename
    urlByUrlId{
      url
    }
  }
}
        `)
          .then(res => {
            this.tileSources = res.pageByPageId.urlByUrlId.url + res.pageByPageId.filename
            this.viewer.open(this.tileSources)
            console.log(this.tileSources)
          })
          .catch(err => {
            console.log('Error.', err)
          })
      }
    }
  }
}
</script>

<style scoped>
.open-sea-dragon{
  width: 100%;
  height: calc(100vh - 200px);
  overflow: hidden;
}
</style>

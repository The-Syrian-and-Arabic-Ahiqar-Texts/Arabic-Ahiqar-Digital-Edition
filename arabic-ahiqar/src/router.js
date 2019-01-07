import Vue from 'vue'
import Router from 'vue-router'
import Spa from '@/components/Spa'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/spa/manuscript-id/:manuscriptID/page-id/:pageID/parallel-group-id/:parallelGroupID',
      name: 'SPA',
      component: Spa
    }
  ]
})

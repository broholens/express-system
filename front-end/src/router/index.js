import Vue from 'vue'
import Router from 'vue-router'
import QueryPrice from '@/components/QueryPrice'
import ImportExpressPrice from '@/components/ImportExpressPrice'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/query-price',
      name: 'QueryPrice',
      component: QueryPrice
    },
    {
      path: '/import-express-price',
      name: 'ImportExpressPrice',
      component: ImportExpressPrice
    }
  ]
})

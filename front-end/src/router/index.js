import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import ImportExpressPrice from '@/components/ImportExpressPrice'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/import-express-price',
      name: 'ImportExpressPrice',
      component: ImportExpressPrice
    }
  ]
})

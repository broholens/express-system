import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import QueryPrice from '@/components/QueryPrice'
import ImportExpressPrice from '@/components/ImportExpressPrice'

Vue.use(Router)

export default new Router({
  mode: 'history',
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
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/',
      name: 'Home',
      component: Home
    }
  ]
})

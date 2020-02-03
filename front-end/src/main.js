// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import axios from 'axios'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import VueCookies from 'vue-cookies'
import Vuex from 'vuex'

Vue.use(ElementUI);
Vue.use(VueCookies)

axios.defaults.withCredentials=true;
axios.defaults.baseURL = 'http://localhost:5000/'
axios.interceptors.request.use(function (config) {
	let token = store.state.token;
	if (token) {
		config.headers['token'] = token;
//    config.headers['Content-Type'] = "application/x-www-form-urlencoded;charset=utf8"
	}
	return config;
})

Vue.prototype.$axios = axios;

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})

export default {
  changeToken (state, token) {
    //登录或者注册时，存储token的方法
    state.token = token
    try {
      sessionStorage.token = token
    } catch (e) {}
  },
  setRole (state, isAdmin) {
    state.isAdmin = isAdmin
    try {
      sessionStorage.isAdmin = isAdmin
    } catch (e) {}
  },
  clearSession (state) {
    sessionStorage.token = ''
    state.token = ''
    sessionStorage.isAdmin = ''
    state.isAdmin = ''
  }
}

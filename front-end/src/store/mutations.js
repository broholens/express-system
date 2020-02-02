export default {
  changeToken (state, token) {
    //登录或者注册时，存储token的方法
    state.token = token
    try {
      localStorage.token = token
    } catch (e) {}
  },
  setRole (state, isAdmin) {
    state.isAdmin = isAdmin
    try {
      localStorage.isAdmin = isAdmin
    } catch (e) {}
  },
  clearSession (state) {
    localStorage.token = ''
    state.token = ''
    localStorage.isAdmin = ''
    state.isAdmin = ''
  }
}

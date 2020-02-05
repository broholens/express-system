// 如果本地缓存里有token，就将token赋值
let defaultToken = ''
let isAdmin = false
try {
  if (localStorage.token) {
    defaultToken = sessionStorage.token
  }
  if (localStorage.isAdmin) {
    isAdmin = sessionStorage.isAdmin
  }
} catch (e) {}

export default {
  token: defaultToken,
  isAdmin: isAdmin
}

<template>
  <el-form class="loginFrom" style="width: 20%" @keyup.enter.native="submitForm">
    <el-input v-model.trim="username" autocomplete="on" clearable placeholder="账号"></el-input>
    <br>
    <br>
    <el-input v-model.trim="password" show-password clearable placeholder="密码"></el-input>
    <br>
    <br>
    <el-button type="primary" size="small" @click="submitForm">提交</el-button>
  </el-form>
</template>

<script>
  import sha256 from 'js-sha256'
  import { Message } from 'element-ui'
  import { mapMutations } from 'vuex'

  export default {
    data() {
      return {
          username: '',
          password: ''
      };
    },
    methods: {
      ...mapMutations([
      				'setRole',
              'changeToken'
      			]),
      submitForm() {
        let self = this;
        let params = new FormData();
        params.append('username', this.username);
        params.append('password', sha256(this.password));
        this.$axios.post('/login', params)
        .then((response) => {
          if (response.status === 200) {
            self.changeToken(response.headers.token);
            self.setRole(response.data.isAdmin);
            self.$router.push("/");
          }
        })
        .catch(function (error) {
          self.$message({
            message: '用户名或密码错误!',
            type: 'error'
          })
        })
      },
    }
  }
</script>
<style scoped>
.loginFrom{
  margin: 0 auto;
}
</style>

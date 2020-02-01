<template>
  <el-form class="loginFrom" style="width: 20%">
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
  import axios from 'axios'
  import { Message } from 'element-ui'
  export default {
    data() {
      return {
          username: '',
          password: ''
      };
    },
    methods: {
      submitForm() {
        let self = this;
        let params = new FormData();
        params.append('username', this.username);
        params.append('password', sha256(this.password));
        console.log(sha256(this.password));
        axios.post('http://localhost:5000/login', params)
        .then((response) => {
          if (response.status === '401') {
            self.$message.error(response.data)
          }else {
            this.$message({
              type: "success",
              message: "OK"
            });
            console.log("ok")
            // self.$router.push("/main");
          }
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

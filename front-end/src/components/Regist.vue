<template>
  <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm" style="width: 20%">
    <el-form-item label="账号" prop="username">
      <el-input v-model.trim="ruleForm.username"></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="pass">
      <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="确认密码" prop="checkPass">
      <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" size="small" @click="submitForm('ruleForm')">注册</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
  import sha256 from 'js-sha256'
  import { Message } from 'element-ui'
  import { mapMutations } from 'vuex'

  export default {
    data() {
      var checkUsername = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('用户名不能为空'))
        }
        // setTimeout(() => {
        if (!this.checkusername(value)) {
          callback(new Error('用户名已存在'));
        }
        // }, 1000)
      };
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (this.ruleForm.checkPass !== '') {
            this.$refs.ruleForm.validateField('checkPass');
          }
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.ruleForm.pass) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
      return {
        ruleForm: {
          pass: '',
          checkPass: '',
          username: ''
        },
        rules: {
          pass: [
            { validator: validatePass, trigger: 'blur' }
          ],
          checkPass: [
            { validator: validatePass2, trigger: 'blur' }
          ],
          username: [
            { validator: checkUsername, trigger: 'blur'}
          ]
        }
      };
    },
    methods: {
      ...mapMutations([
      				'setRole',
              'changeToken'
            ]),
      checkusername(value) {
        let params = new FormData();
        params.append('username', value);
        console.log(value);
        console.log(params.get('username'));
        this.$axios.post('/is-user-exists', params)
        .then((response) => {
          console.log(response.data);
          if (!response.data.isExists) {
            console.log('return true')
            return true
          }else {
            return false
          }
        })
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.regist();
          }
        });
      },
      regist() {
        let self = this;
        let params = new FormData();
        params.append('username', self.ruleForm.username);
        params.append('password', sha256(self.ruleForm.pass));
        this.$axios.post('/register', params)
        .then((response) => {
          if (response.status === 200) {
            self.changeToken(response.headers.token);
            self.setRole(response.data.isAdmin);
            self.$router.push("/");
          }
        })
        .catch(function (error) {
          self.$message({
            message: '用户名已存在!',
            type: 'error'
          })
        })
      }
    }
  }
</script>

<style scoped>
.loginFrom{
  margin: 0 auto;
}
</style>
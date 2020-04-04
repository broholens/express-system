<template>
  <div style="width: 20%; margin:0 auto">
    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
      <el-form-item label="账号" prop="username">
        <el-input v-model.trim="ruleForm.username"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="pass">
        <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="checkPass">
        <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="验证码" prop="captcha">
        <el-input v-model="ruleForm.captcha" autocomplete="off" maxlength=4 style="float: left; width: 122px;"></el-input>
        <div>
          <img src="" ref="code" @click="ChangeCode">
        </div>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" size="small" @click="submitForm('ruleForm')">注册</el-button>
      </el-form-item>
    </el-form>
  </div>
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
        setTimeout(() => {
          this.checkusername(value)
          .then((response) => {
            console.log(response.data)
            if (response.data.isExists) {
              callback(new Error('用户名已存在'));
            }else {
              // 没有callback的话会一直转圈
              callback()
            }
          })
        }, 1000)
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
      var checkCode = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('验证码不能为空'));
        } else if (sha256(value) !== this.captcha_code) {
          callback(new Error('验证码错误'));
        } else {
          callback();
        }
      };
      return {
        captcha_code: '',
        ruleForm: {
          pass: '',
          checkPass: '',
          username: '',
          captcha: ''
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
          ],
          captcha: [
            { validator: checkCode, trigger: 'blur' }
          ]
        }
      };
    },
    mounted() {
      this.changeCode()
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
        return this.$axios.post('/is-user-exists', params)
      },
      changeCode() {
        this.$axios.get('/generate-captcha-code')
        .then((response) => {
          this.captcha_code = response.data.captcha;
          this.$refs.code.setAttribute(
            "src",
            "../../../"+this.captcha_code+'.png'
          )
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
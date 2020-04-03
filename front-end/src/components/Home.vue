<template>
  <el-row>
    <el-col v-if="haveToken" :span="4">
      <h5>菜单</h5>
      <el-menu
        class="el-menu-vertical-demo">
        <el-menu-item index="1" @click="toQueryPrice">
          <i class="el-icon-search"></i>
          <span slot="title">查询价格</span>
        </el-menu-item>
        <el-menu-item v-if="isAdmin" index="2" @click="toImportExpressPrice">
          <i class="el-icon-circle-plus-outline"></i>
          <span slot="title">导入价格</span>
        </el-menu-item>
        <el-menu-item index="3" disabled>
          <i class="el-icon-setting"></i>
          <span slot="title">研制ing...</span>
        </el-menu-item>
      </el-menu>
    </el-col>
    <el-col v-else>
      <el-button type="primary" @click="toLogin">登录</el-button>
      <el-button type="primary" @click="toRegist">注册</el-button>
    </el-col>
  </el-row>
</template>

<script>
  export default {
    data() {
      return {
        haveToken: this.$store.state.token!=='',
        isAdmin: !this.haveToken && this.$store.state.isAdmin
      }
    },
    methods: {
      toImportExpressPrice() {
        this.$router.push('/import-express-price')
      },
      toQueryPrice() {
        this.$router.push('/query-price')
      },
      toLogin() {
        this.$router.push('/login')
      },
      toRegist() {
        this.$router.push('/regist')
      }
    }
  }
</script>

<style>
  .el-header, .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }

  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
  }

  body > .el-container {
    margin-bottom: 40px;
  }

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>

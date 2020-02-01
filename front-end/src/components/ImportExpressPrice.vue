<template>
  <div>
    <el-upload
      class="import-express-price"
      action="doUpload"
      :before-upload="beforeUpload"
      :http-request="submitUpload"
      :limit="1">
      <i v-if="ready" class="el-icon-circle-plus-outline"></i>
      <i v-if="loading" class="el-icon-loading"></i>
    </el-upload>
  </div>
</template>
<script>
  import axios from 'axios'
  import { Message } from 'element-ui'

  export default {
    data() {
      return {
        files: [],
        fileList: [],
        fileName: "",
        file: "",
        ready: true,
        loading: false
      }
    },
    methods: {
      beforeUpload(file) {
        this.file = file;
        this.fileName = this.file.name;
      },
      doUpload() {},
      submitUpload() {
        let fileFormData = new FormData();
        fileFormData.append('file', this.file);
        let requestConfig = {
          headers: {'Content-Type': 'multipart/form-data'}
        }
        axios.post('http://localhost:5000/import-express-price', fileFormData, requestConfig).then((response) => {
          this.ready = true;
          this.loading = false;
          if (response.status === 200) {
            this.$message({
              message: '操作成功',
              type: 'success'
            })
          }
        })
        this.ready = false;
        this.loading = true;
      }
    }
  }
</script>

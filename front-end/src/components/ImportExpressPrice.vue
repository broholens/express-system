<template>
  <div>
    <el-upload
      class="import-express-price"
      action="doUpload"
      drag
      :before-upload="beforeUpload"
      :http-request="submitUpload"
      :limit="1">
      <i class="el-icon-upload"></i>
      <h2 v-if="loading" class="el-icon-loading"></h2>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
    </el-upload>
    <br>
    <br>
    <a class="download" download="" href="../../static/data/express_price.xlsx" target="_blank">下载模板</a>
  </div>
  <!-- <div>
    <el-upload
      class="upload-demo"
      drag
      action="/import-express-price"
      multiple>
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过500kb</div>
    </el-upload>
  </div> -->
</template>
<script>
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
        this.$axios.post('/import-express-price', fileFormData, requestConfig).then((response) => {
          this.loading = false;
          if (response.status === 200) {
            this.$message({
              message: '上传成功',
              type: 'success'
            })
          }else {
            this.$message({
              message: '解析失败, 请检查文件格式',
              type: 'error'
            })
          }
        })
        this.loading = true;
      }
    }
  }
</script>

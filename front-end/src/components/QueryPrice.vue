<template>
  <div>
    <el-row class="address">
      <el-col :span="8">
        <el-autocomplete
          class="inline-input"
          v-model="from_"
          :fetch-suggestions="querySearch"
          placeholder="始发地"
          @select="handleFrom"
        ></el-autocomplete>
      </el-col>
      <el-col :span="8">
        <el-autocomplete
          class="inline-input"
          v-model="to_"
          :fetch-suggestions="querySearch"
          placeholder="目的地"
          @select="handleTo"
        ></el-autocomplete>
      </el-col>
      <el-col :span="8">
        <el-input class="inline-input" v-model="weight" placeholder="重量"></el-input>
      </el-col>
    </el-row>
    <el-button type="primary" icon="el-icon-search" @click="query">查询</el-button>
  </div>
</template>
<script>
  import axios from 'axios'
  import qs from 'qs'
  import { Message } from 'element-ui'

  export default {
    data() {
      return {
        countries: [],
        from_: '',
        to_: '',
        weight: ''
      };
    },
    methods: {
      querySearch(queryString, cb) {
        var countries = this.countries;
        var results = queryString ? countries.filter(this.createFilter(queryString)) : countries;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      createFilter(queryString) {
        return (country) => {
          return (country.value.toLowerCase().indexOf(queryString.toLowerCase()) !== -1);
        };
      },
      handleFrom(item) {
        this.from_ = item;
      },
      handleTo(item) {
        this.to_ = item;
      },
      query() {
        let self = this;
        let params = {
          "from_": this.from_,
          "to_": this.to_,
          "weight": this.weight
        }
        axios.post('http://localhost:5000/query', qs.stringify(params)).then((response) => {
          if (response.status === 200) {
            console.log(response.data.expressList)
          }
        })
      }
    },
    mounted() {
      // let self = this;
      axios.get('http://localhost:5000/countries').then((response) => {
        if (response.status === 200) {
          // 自动补全的返回值里面必须包含value
          // var respCountries = response.data.countries;
          // console.log(respCountries);
          // var countries = [];
          // for (var i in respCountries) {
          //   countries.push({"value": respCountries[i]});
          // }
          // console.log(countries);
          this.countries = response.data.countries;
        }
      })
    }
  }
</script>

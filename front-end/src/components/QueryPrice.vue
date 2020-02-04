<template>
  <div>
    <el-row class="address">
      <el-col :span="8">
        <el-autocomplete
          class="inline-input"
          clearable
          v-model="from_"
          :fetch-suggestions="querySearch"
          placeholder="始发地"
          @select="handleFrom"
        ></el-autocomplete>
      </el-col>
      <el-col :span="8">
        <el-autocomplete
          class="inline-input"
          clearable
          v-model="to_"
          :fetch-suggestions="querySearch"
          placeholder="目的地"
          @select="handleTo"
        ></el-autocomplete>
      </el-col>
      <el-col :span="8">
        <el-input class="inline-input" clearable v-model="weight" placeholder="重量"></el-input>
      </el-col>
    </el-row>
    <br>
    <el-button type="primary" icon="el-icon-search" @click="query">查询</el-button>
    <br>
    <br>
    <el-table
        v-if="seen"
        align="center"
        :data="queriedData"
        style="width: 100%"
        :default-sort = "{prop: 'price', order: 'descending'}"
        >
        <el-table-column
          prop="name"
          label="运输渠道"
          width="180">
        </el-table-column>
        <el-table-column
          prop="to_"
          label="目的地"
          width="90">
        </el-table-column>
        <el-table-column
          prop="weight"
          label="重量(KG)"
          width="90">
        </el-table-column>
        <el-table-column
          prop="price_formula"
          label="价格公式"
          width="180">
        </el-table-column>
        <el-table-column
          prop="total_price"
          label="总价"
          sortable
          width="160">
        </el-table-column>
        <el-table-column
          prop="price"
          label="换算后单价"
          sortable
          width="160">
        </el-table-column>
        <el-table-column
          prop="currency"
          label="币种"
          width="80">
        </el-table-column>
        <el-table-column
          prop="remarks"
          label="备注"
          width="240">
        </el-table-column>
      </el-table>
  </div>
</template>
<script>
  import qs from 'qs'
  import { Message } from 'element-ui'

  export default {
    data() {
      return {
        countries: [],
        from_: '',
        to_: '',
        weight: '',
        queriedData: [],
        seen: false
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
        // 要带value, [Vue warn]: Invalid prop: type check failed for prop "value". Expected String, get object.
        this.from_ = item.value;
      },
      handleTo(item) {
        this.to_ = item.value;
      },
      query() {
        let self = this;
        let params = {
          "from_": this.from_,
          "to_": this.to_,
          "weight": this.weight
        }
        this.$axios.post('/query', qs.stringify(params)).then((response) => {
          if (response.status === 200) {
            self.seen = true;
            self.queriedData = response.data.expressList;
          }
        })
      }
    },
    mounted() {
      let self = this;
      this.$axios.get('/countries').then((response) => {
        if (response.status === 200) {
          // 自动补全的返回值里面必须包含value
          self.countries = response.data.countries;
        }
      })
    }
  }
</script>

<template>
  <div>
    <Navbar />
    <div class="statistic-main">
      <div class="top_statistic">
        <p class="h1">HO statistic</p>
        <HOStatistic />
      </div>
      <div class="statistic-main-top">
        <div class="statistic-main-top-left">
          <div
            class="h1"
            style="padding: 5px 0px 15px 20px; width: fit-content; float: left"
          >
            <font-awesome-icon
              icon="fa-solid fa-file-excel"
              style="color: #026600"
              size="2xl"
              class="btn-export"
              @click="handleExportAPI"
            />
            Inspection
          </div>
          <div
            class="form-input"
            style="width: 250px; float: right; padding: 5px 50px 15px 0"
          >
            <input type="text" placeholder="Enter key" v-model="keySearch" />
          </div>
          <v-progress-linear
            indeterminate
            color="#026600"
            v-if="this.loading"
          ></v-progress-linear>
          <table>
            <thead>
              <th @click="sortPa('id')" style="padding-left: 20px">
                <font-awesome-icon
                  icon="fa-solid fa-sort"
                  style="color: #3d555426"
                />
                ID
              </th>
              <th>Status OK</th>
              <th>From</th>
              <th>To</th>
            </thead>
            <tbody>
              <tr
                v-for="item in sortListPa"
                :key="item.id"
                @click="getDetail(item.id)"
              >
                <td>
                  <p class="content-start">{{ item["id"] }}</p>
                </td>
                <td v-if="item['state_ok'] < 20">
                  <p style="color: red; font-weight: 800">
                    {{ item["state_ok"] }}%
                  </p>
                </td>
                <td v-else-if="item['state_ok'] > 50">
                  <p style="color: rgb(0, 123, 255)">{{ item["state_ok"] }}%</p>
                </td>
                <td v-else>
                  <p>{{ item["state_ok"] }}%</p>
                </td>
                <td>
                  <p>{{ item["begin"] }}</p>
                </td>
                <td>
                  <p>{{ item["end"] }}</p>
                </td>
                <td>
                  <p class="content-end">
                    <font-awesome-icon
                      icon="fa-solid fa-chevron-right"
                      style="color: #3d5554"
                    />
                  </p>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="footer-table" v-if="this.listInspection.length > 10">
            <button @click="prevPagePa" v-if="this.currentPagePa != 1">
              <font-awesome-icon
                icon="fa-solid fa-chevron-left"
                size="2xl"
                style="color: #3d5554"
              />
            </button>
            <p>{{ this.currentPagePa }}</p>
            <button
              @click="nextPagePa"
              v-if="this.currentPagePa * 10 < this.listInspection.length"
            >
              <font-awesome-icon
                icon="fa-solid fa-chevron-right"
                size="2xl"
                style="color: #3d5554"
              />
            </button>
          </div>
        </div>
        <div
          class="statistic-main-top-right"
          v-if="this.currentId != 'Undefined'"
        >

        <div height="500" >
            <PredictStatistic />
          </div>
          <div height="500dp" >
            <DoughnutChart />
          </div>
          
        </div>
        <div class="statistic-main-top-rignt" v-else></div>
      </div>
      <div class="statistic-main-bottom">
        <div
          class="statistic-main-bottom-content"
          v-if="this.$store.state.chartDashboard.angleId != null"
        >
          <download-excel
            class="btn btn-default"
            :data="listAllDetails"
            :fields="json_fields"
            :worksheet="currentId"
            :name="fileNameID"
          >
            <div class="h1" style="margin: 5px 0 15px 20px; width: fit-content">
              <font-awesome-icon
                icon="fa-solid fa-file-excel"
                style="color: #026600"
                size="2xl"
                class="btn-export"
              />
              {{ this.currentId }}
            </div>
          </download-excel>
          <table>
            <thead>
              <th style="padding-left: 20px">Date</th>
              <th>Time</th>
              <th @click="sortCh('angle_id')">
                <font-awesome-icon
                  icon="fa-solid fa-sort"
                  style="color: #3d555426"
                />
                Angle_id
              </th>
              <th>Status</th>
              <th>Predict_result</th>
            </thead>
            <tbody>
              <tr v-for="item in sortListCh" :key="item.id">
                <td>
                  <p class="content-start">{{ item["date"] }}</p>
                </td>
                <td>
                  <p>{{ item["time"] }}</p>
                </td>
                <td>
                  <p>{{ item["angle_id"] }}</p>
                </td>
                <td>
                  <p
                    v-if="item['status'] === 'ok'"
                    style="color: #58d68d; font-weight: 800"
                  >
                    {{ item["status"] }}
                  </p>
                  <p v-else>
                    {{ item["status"] }}
                  </p>
                </td>
                <td>
                  <p>{{ item["predict_result"] }}</p>
                </td>
              </tr>
            </tbody>
          </table>
          <div
            class="footer-table"
            v-if="this.listAllDetails.length > this.pageSize"
          >
            <button @click="prevPageCh" v-if="this.currentPageCh != 1">
              <font-awesome-icon
                icon="fa-solid fa-chevron-left"
                size="2xl"
                style="color: #3d5554"
              />
            </button>
            <p>{{ this.currentPageCh }}</p>
            <button
              @click="nextPageCh"
              v-if="this.currentPageCh * 10 < this.listAllDetails.length"
            >
              <font-awesome-icon
                icon="fa-solid fa-chevron-right"
                size="2xl"
                style="color: #3d5554"
              />
            </button>
          </div>
          <div class="footer-table" v-else style="padding-bottom: 20px"></div>
        </div>
        <div class="statistic-main-bottom-content" v-else>
          <p class="note">Click row to show chart !</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { GET_INSPECTION, GET_INSPECTION_DETAIL } from "@/axios";
import Navbar from "../../AppNav.vue";
import DoughnutChart from "./charts/DoughnutChart.vue";
import HOStatistic from "./charts/HOStatistic.vue";
import PredictStatistic from "./charts/PredictStatistic.vue";
import { EXPORT_EXCEL_API, GET_HO_STATISTIC } from "../../../axios";

export default {
  name: "StatisticPage",
  components: {
    Navbar,
    DoughnutChart,
    HOStatistic,
    PredictStatistic,
  },
  data() {
    return {
      listInspection: [],
      listAllDetails: [],
      pageSize: 10,
      currentPagePa: 1,
      currentPageCh: 1,
      sortByPa: "id",
      sortOrderPa: 1,
      sortByCh: "id",
      sortOrderCh: 1,
      keySearch: "",
      currentId: "Undefined",
      loading: false,
      json_fields: {
        Date: "date",
        Time: "time",
        Angle_id: "angle_id",
        Status: "status",
        Predict_result: "predict_result",
      },
      json_meta: [
        [
          {
            key: "charset",
            value: "utf-8",
          },
        ],
      ],
      fileNameID: "Undefined",
    };
  },
  mounted() {
    if (
      localStorage.getItem("id") == null ||
      localStorage.getItem("access_token") == null
    ) {
      this.$router.push({ name: "Signin" });
    }
  },
  async created() {
    this.$store.commit("isStatistic");
    this.$store.dispatch("angleId", null);

    await axios.get(GET_INSPECTION).then((res) => {
      if (res.status == 200) {
        this.listInspection = res.data.data;
      }
    });

    await axios.get(GET_HO_STATISTIC).then((res) => {
      if (res.status == 200) {
        this.$store.dispatch("labels", res.data.label);
        this.$store.dispatch("values", res.data.value);
      }
    });
  },
  methods: {
    nextPagePa() {
      if (this.currentPagePa * this.pageSize < this.listInspection.length)
        this.currentPagePa++;
    },
    prevPagePa() {
      if (this.currentPagePa > 1) this.currentPagePa--;
    },

    nextPageCh() {
      if (this.currentPageCh * this.pageSize < this.listAllDetails.length)
        this.currentPageCh++;
    },
    prevPageCh() {
      if (this.currentPageCh > 1) this.currentPageCh--;
    },
    sortPa(sortByPa) {
      if (this.sortByPa === sortByPa) {
        this.sortOrderPa = -this.sortOrderPa;
      } else {
        this.sortByPa = sortByPa;
      }
    },
    sortCh(sortByCh) {
      if (this.sortByCh === sortByCh) {
        this.sortOrderCh = -this.sortOrderCh;
      } else {
        this.sortByCh = sortByCh;
      }
    },
    async getDetail(id) {
      await axios
        .get(GET_INSPECTION_DETAIL, { params: { id: id } })
        .then((res) => {
          if (res.status == 200) {
            this.$store.dispatch("angleId", res.data.angle_id);
            this.$store.dispatch("predicts", res.data.label);
            this.$store.dispatch("predict_values", res.data.value);
            this.listAllDetails = res.data.all_details;
            this.currentId = id;
            this.fileNameID = id + ".xls";
          }
        })
        .catch((ex) => console.log(ex));
    },
    async handleExportAPI() {
      this.loading = true;
      await axios
        .get(EXPORT_EXCEL_API, {
          responseType: "blob",
        })
        .then((res) => {
          if (res.status == 200) {
            // Let's create a link in the document that we'll
            // programmatically 'click'.
            const link = document.createElement("a");

            // Tell the browser to associate the response data to
            // the URL of the link we created above.
            link.href = window.URL.createObjectURL(new Blob([res.data]));

            // Tell the browser to download, not render, the file.
            link.setAttribute("download", "api_data.xlsx");

            // Place the link in the DOM.
            document.body.appendChild(link);

            // Make the magic happen!
            link.click();
            this.loading = false;
          }
        })
        .catch((ex) => {
          console.log(ex);
        });
    },
  },
  computed: {
    // sortListPa() {
    //   return this.listInspection.filter((row, index) => {
    //     let start = (this.currentPagePa - 1) * this.pageSize;
    //     let end = this.currentPagePa * this.pageSize;
    //     if (index >= start && index < end) return true;
    //   });
    // },
    sortListPa() {
      return [...this.listInspection]
        .sort((a, b) => {
          if (a[this.sortByPa] >= b[this.sortByPa]) {
            return this.sortOrderPa;
          }
          return -this.sortOrderPa;
        })
        .filter((row) => {
          if (this.keySearch.toLowerCase() != "") {
            if (this.keySearch.includes("%"))
              return row.state_ok == this.keySearch.toLowerCase().replace("%", "");
            return row.id.includes(this.keySearch.toLowerCase());
          }
          return true;
        })
        .filter((row, index) => {
          let start = (this.currentPagePa - 1) * this.pageSize;
          let end = this.currentPagePa * this.pageSize;

          if (index >= start && index < end) return true;
        });
    },
    sortListCh() {
      return [...this.listAllDetails]
        .sort((a, b) => {
          if (a[this.sortByCh] >= b[this.sortByCh]) {
            return this.sortOrderCh;
          }
          return -this.sortOrderCh;
        })
        .filter((row, index) => {
          let start = (this.currentPageCh - 1) * this.pageSize;
          let end = this.currentPageCh * this.pageSize;
          if (index >= start && index < end) return true;
        });
    },
  },
  watch: {
    keySearch() {
      this.sortListPa;
    },
  },
};
</script>
<style >
@import url("../../../assets/css/nav-style.css");
@import url("../../../assets/css/statistic-style.css");
</style>
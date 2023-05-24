<template>
  <div>
    <div class="navcontain">
      <div class="header-name-page">{{ msgSignUp }}</div>
    </div>
    <div class="contain">
      <form @submit.prevent="handlerSubmit">
        <div>
          <img
            src="../../../assets/images/check.png"
            alt="Login"
            width="100px"
            height="100px"
          />
        </div>
        <input
          type="otp"
          v-model="otp"
          placeholder="Enter OTP"
          name="otp"
          required
        />

        <button>Verify</button>
      </form>
    </div>
  </div>
</template>
<script>
import axios from "axios";

import { VERIFY } from "@/axios";
export default {
  name: "VerifyAccountPage",
  data() {
    return {
      msgSignUp: "Verify Account",
      otp: "",
    };
  },
  methods: {
    async handlerSubmit() {
      await axios
        .post(VERIFY, { email: localStorage.getItem("email"), code: this.otp })
        .then((res) => {
          if (res.status == 200) {
            localStorage.setItem("id", res.data.data.id);
            localStorage.setItem("email", res.data.data.email);
            localStorage.setItem("role", res.data.data.role);
            localStorage.setItem("access_token", res.data.access_token);

            axios.defaults.headers.common[
              "Authorization"
            ] = `Bearer ${res.data.access_token}`;

            this.$router.push({ name: "Signin" });
          }
        })
        .catch((ex) => {
          if (ex.response.status == 307) {
            console.log(ex.response.data.detail.access_token)
            localStorage.setItem("access_token", ex.response.data.detail.access_token);
            axios.defaults.headers.common[
              "Authorization"
            ] = `Bearer ${ex.response.data.detail.access_token}`;
           this.$router.push({name:"ChangePassword"})
          }
        });
    },
  },
};
</script>
<style>
@import url("../../../assets/css/nav-style.css");
@import "../../../assets/css/form-style.css";
</style>
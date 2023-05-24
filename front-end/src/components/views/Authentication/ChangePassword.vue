<template>
  <div>
    <div class="changepassword">
      <div class="contain-input">
        <input
          type="password"
          :placeholder="this.label.pw"
          id="inputPW"
          required
        />
        <input
          type="password"
          :placeholder="this.label.cpw"
          id="inputPW2"
          required
        />
        <span id="notify-error"></span>
        <button @click.prevent="handleChange">Change</button>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { UPDATE_PASSWORD } from "../../../axios";

export default {
  name: "ChangePassword",
  data() {
    return {
      label: {
        pw: "Password",
        cpw: "Confirm password",
      },
      email: localStorage.getItem("email"),
    };
  },
  components: {},
  mounted() {
    if (localStorage.getItem("access_token") == null) {
      this.$router.push({ name: "Signin" });
    }
  },
  created() {
    this.$store.commit("isProfile");
  },
  methods: {
    async handleChange() {
      var pw = document.getElementById("inputPW").value;
      var pw2 = document.getElementById("inputPW2").value;

      if (pw == pw2 && pw != "") {
        const regex =
          /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@#$%^&*()_+!])(?=.*[a-zA-Z\d@#$%^&*()_+!]).{8,}$/;
        if (regex.test(pw)) {
          await axios
            .put(UPDATE_PASSWORD, {
              email: localStorage.getItem("email"),
              password: pw,
            })
            .then((res) => {
              if (res.status == 200) {
                this.$router.push({ name: "Profile" });
              }
            })
            .catch((ex) => {
              if (ex.response.status == 401) {
                this.$router.push({ name: "Signin" });
              }
            });
        } else {
          document.getElementById("notify-error").innerHTML =
            "Invalid password";
        }
      } else if (pw != " ") {
        document.getElementById("notify-error").innerHTML = "Enter password";
      } else {
        document.getElementById("notify-error").innerHTML =
          "Password do NOT match!";
      }
    },
  },
};
</script>

<style>
@import url("../../../assets/css/nav-style.css");
@import url("../../../assets/css/changepassword-style.css");
</style>

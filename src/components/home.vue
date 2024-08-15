<template>
  <div class="container">
    <div id="box">
      <input
        type="text"
        id="search"
        placeholder="Search"
        @input="search($event)"
      />
      <div id="list">
        <button
          v-for="i in data"
          :key="i"
          class="names"
          @click="clicked(i.CODE)"
        >
          {{ i.NAME }}
        </button>
      </div>
      <div id="bottom-box">
        <button @click="$router.push('/create')">Add</button>
        <!-- <button disabled>Modify</button>
        <button disabled>Delete</button> -->
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  data() {
    return {
      data: ref([]),
    };
  },
  methods: {
    search(e) {
      fetch(`http://127.0.0.1:5000/home`, {
        method: "POST",
        body: JSON.stringify({ search: e.target.value }), // Note the .value, as data is a ref
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (!response.ok) {
            console.error("Error fetching data:", response.statusText);
            throw new Error("HTTP " + response.status);
          }
          return response.json(); // Return the parsed JSON data
        })
        .then((data) => {
          console.log(data);
          this.data = data;
        })
        .catch((error) => {
          console.error("An error occurred:", error);
        });
    },
    clicked(code) {
      this.$router.push("/company");
      alert("clicked");
      let data = {
        code: code,
        fy: "unset"
      }
      this.$cookies.set("code", data);
      console.log(this.$cookies.get(code));
    },
    getData() {
      // CHANGE IP HERE
      fetch("http://127.0.0.1:5000/home")
        .then((response) => {
          if (!response.ok) {
            console.error("Error fetching data:", response.statusText);
            throw new Error("HTTP " + response.status);
          }
          return response.json(); // Return the parsed JSON data
        })
        .then((data) => {
          console.log(data);
          this.data = data;
        })
        .catch((error) => {
          console.error("An error occurred:", error);
        });
    },
  },
  mounted() {
    this.getData(); // Call the method when the component is mounted
  },
};
</script>

<style>
:root {
  --var-dark: #161A30;
  --var-light: #F0ECE5;
  --var-blue: #B6BBC4;
  --var-mid: #31304D;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
#search {
  width: 570px;
  height: 35px;
  padding: 5px;
  border: 1px white solid;
  background-color: var(--var-light);
  border-radius: 15px;
  color: black;
}
#search::placeholder {
  text-align: center;
}
.container {
  display: flex;
  height: 100vh;
  width: 100vw;
  justify-content: center;
  align-items: center;
  background-color: var(--var-dark);
}
#box {
  width: 600px;
  height: 600px;
  background: var(--var-mid);
  border: 1px white solid;
  border-radius: 15px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  justify-content: space-evenly;
}
#list {
  display: flex;
  flex-direction: column;
  border-radius: 15px;
  padding: 15px;
  gap: 15px;
  width: 570px;
  height: 480px;
  background: var(--var-blue);
  overflow-y: scroll;
}
.names {
  width: 500px;
  height: 100px;
  padding: 15px;
  border: 1px var(--var-mid) solid;
  background-color: white;
  border-radius: 15px;
}
.names:hover {
  background: var(--var-mid);
  color: white;
}
#bottom-box {
  background-color: var(--var-light);
  border-radius: 15px;
  width: 570px;
  height: 50px;
  padding: 15px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  align-items: center;
  gap: 5px;
}
#bottom-box > button {
  flex-basis: 65%;
  height: 40px;
  border: 1px #ffc470 solid;
  border-radius: 15px;
  background: var(--var-blue);
}
#bottom-box button:hover {
  background: var(--var-mid);
  color: white;
}
</style>

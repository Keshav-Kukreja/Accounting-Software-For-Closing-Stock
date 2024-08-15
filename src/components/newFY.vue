<template>
  <div class="container">
    <div>
      <div v-if="ready" id="info">
        <div id="comp_name">{{ company.name }}</div>
        <div>
          <div id="newfy" style="color: black;">New F.Y. : {{ fy }}</div>
        </div>
        <div id="note">
          <p>
            To proceed with new F.Y. click "Create" and to go back to the
            previous page click "Cancel"
          </p>
        </div>
        <div id="btns-box">
          <button @click="postData({code: company.code, fy: fy})">Create</button>
          <button @click="$router.go(-1)">Cancel</button>
        </div>
      </div>
      <h1 v-else>{{ message.value }}</h1>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from 'vue-router';
const router = useRouter();
const ready = ref(false);
const company = ref(null);
const fy=ref('');
const message = ref("Loading...");

const code = ref($cookies.get("code").code);

fetch(`http://127.0.0.1:5000/code/${code.value}`, {
  method: "GET",
})
  .then((response) => {
    if (!response.ok) {
      console.error("Error fetching data:", response.statusText);
      throw new Error("HTTP " + response.status);
    }
    return response.json(); // Return the parsed JSON data
  })
  .then((data) => {
    company.value = data;
    console.log(data);
    setTimeout(() => {
        ready.value = true;
        fy.value=parseInt(company.value.fy[company.value.fy.length - 1])+1
    }, 1000);
  })
  .catch((error) => {
    console.error("An error occurred:", error);
  });

  const postData = (val) => {
    console.log(val);
   fetch(`http://127.0.0.1:5000/new_fy`, {
     method: "POST",
     body: JSON.stringify(val), // Note the .value, as data is a ref
     headers: {
       "Content-Type": "application/json",
     }
   }).then((res) => {
     return res.json();
   }).then((data) => {
     //console.log(data);
     message.value = data.message;
     ready.value = false;
     setTimeout(() => {
       router.go(-1);
     }, 1500)
   })
};
</script>

<style scoped>
#info {
  width: 600px;
  height: 400px;
  border: 2px solid var(--var-mid);
  border-radius: var(--var-radius);
  display: flex;
  flex-direction: column;
  background-color: white;
  justify-content: start;
  align-items: center;
  gap: 5px;
  padding: 10px;
}

#newfy,
#comp_name {
  width: 550px;
  height: 50px;
  text-align: center;
  background-color: var(--var-blue);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: var(--var-radius);
  text-align: center;
  font-size: 18pt;
}
#comp_name {
  background-color: var(--var-mid);
}

#note {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 550px;
  height: 180px;
  font-size: 20pt;
  background-color: var(--var-blue);
  border-radius: var(--var-radius);
  border: 1px solid var(--var-mid);
  text-align: center;
}
#btns-box {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
  width: 550px;
  height: 80px;
  background-color: var(--var-blue);
  border-radius: var(--var-radius);
}
#btns-box > button {
    flex-basis: 45%;
    height: 50px;
    border: 1px solid var(--var-mid);
    border-radius: var(--var-radius);
}
#btns-box > button:hover {
  background-color: var(--var-mid);
}
</style>

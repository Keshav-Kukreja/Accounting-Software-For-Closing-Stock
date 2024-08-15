<script setup>
// import section
import { ref } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();

// variable section
const ready = ref(false);
const exportBtnText = ref("Export");
const company = ref(null);
const cy = ref(null);
const code = ref($cookies.get("code").code);

const total = (val) => {
  let total = 0;
  for (let key in company.value.Discription) {
    const subObj = company.value.Discription[key];
    total += parseInt(subObj[val]);
  }
  return total;
};

const url = "http://127.0.0.1:5000"

// function section

// this function fetch the data from the server
// change ip to make it work
fetch(`${url}/code/${code.value}`, {
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
    company.value = data; // Assign the data to the ref
    cy.value = data.fy[0];
    setTimeout(() => {
      ready.value = true;
    }, 2000);
  })
  .catch((error) => {
    console.error("An error occurred:", error);
  });

// this function post data to the server
const getDiscription = (val) => {
  cy.value = val.fy;
  if (val.fy != "New") {
    fetch(`${url}/code/${code.value}`, {
      method: "POST",
      body: JSON.stringify(val), // Note the .value, as data is a ref
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        company.value = data;
        console.log(data);
      });
  } else {
    router.push("/newFY");
  }
};

const saveData = () => {
  fetch(`${url}/save`, {
    method: "POST",
    body: JSON.stringify({ company: company.value, cy: cy.value }), // Note the .value, as data is a ref
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      alert("Saved");
      console.log(data);
    });
};

const download = () => {
  fetch(`${url}/generate`, {
    method: "POST",
    body: JSON.stringify({ code: code.value, fys: company.value.fy, name: company.value.name }), // Note the .value, as data is a ref
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      exportBtnText.value = "Downloading...";
      setTimeout(() => {
        window.location.href = `${url}/download/${code.value}`;
        exportBtnText.value = "Export";
      }, 1500);
    });
};

// btn click
// const clicked = () => {
//   console.log(company);
//   alert("clicked");
// };

const ClearData = () => {
  for (let key in company.value.Discription) {
    company.value.Discription[key].OS = 0;
    company.value.Discription[key].Pur = 0;
    company.value.Discription[key].GP = 0;
    company.value.Discription[key].Sale = 0;
  }
};

const GrossProfit = (e, index) => {
  if (e.target.value.includes("%")) {
    let value = e.target.value.replace("%", "");
    value = parseFloat(value);
    value = (value / 100) * parseFloat(company.value.Discription[index].Sale);
    company.value.Discription[index].GP = parseInt(value);
    console.log(company.value.Discription[index].GP);
  }
};

const setCookies = () => {
  // Use setCookie instead of this.$cookies.set
  $cookies.set('code', { code: code.value, fy: cy.value });
  alert($cookies.get('code')); // Use getCookie instead of this.$cookies.get
  console.log($cookies.get('code'));
  router.push("/modify");
};

</script>

<template>
  <div class="container1" v-if="ready">
    <div class="top">
      <h1>{{ company.name }}</h1>
      <select
        @change="getDiscription({ fy: $event.target.value })"
        name=""
        id=""
        style="
          width: 600px;
          text-align: center;
          padding: 5px;
          border-radius: 8px;
        "
      >
        <option v-for="i in company.fy" :key="i" :value="i">{{ i }}</option>
        <option value="New">New F.Y.</option>
      </select>
    </div>
    <div style="height: 100%; overflow-x: auto;">
    <table style="height: 100%; width: 100%;">
      <tbody>
        <th>Discription</th>
        <th>Opening Stock</th>
        <th>Purchase</th>
        <th>Gross Profit</th>
        <th>Sale</th>
        <th>Closing Stock</th>
        <tr v-for="(item, index) in company.Discription" :key="index">
          <td>{{ item.Tax }}</td>
          <td>
            <input
              type="text"
              v-model="company.Discription[index].OS"
              @input="company.Discription[index].OS = $event.target.value"
            />
          </td>
          <td>
            <input
              type="text"
              v-model="company.Discription[index].Pur"
              @input="company.Discription[index].Pur = $event.target.value"
            />
          </td>
          <td>
            <input
              type="text"
              v-model="company.Discription[index].GP"
              @input="GrossProfit($event, index)"
            />
          </td>
          <td>
            <input
              type="text"
              v-model="company.Discription[index].Sale"
              @input="company.Discription[index].Sale = $event.target.value"
            />
          </td>
          <td>
            <input
              type="text"
              :value="
                (company.Discription[index].CS =
                  parseInt(company.Discription[index].OS) +
                  parseInt(company.Discription[index].Pur) +
                  parseInt(company.Discription[index].GP) -
                  parseInt(company.Discription[index].Sale))
              "
              readonly
            />
          </td>
        </tr>
        <tr>
          <td>Total</td>
          <td>
            <input
              type="text"
              :value="(company.total.OS = total('OS'))"
              readonly
            />
          </td>
          <td>
            <input
              type="text"
              :value="(company.total.Pur = total('Pur'))"
              readonly
            />
          </td>
          <td>
            <input
              type="text"
              :value="(company.total.GP = total('GP'))"
              readonly
            />
          </td>
          <td>
            <input
              type="text"
              :value="(company.total.Sale = total('Sale'))"
              readonly
            />
          </td>
          <td>
            <input
              type="text"
              :value="
                (company.total.CS =
                  total('OS') + total('Pur') + total('GP') - total('Sale'))
              "
              readonly
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
    <div class="options">
      <button @click="$router.go(-1)">Back</button>
      <button @click="ClearData">Clear</button>
      <button :onclick="saveData">Save</button>
      <button @click="download">{{ exportBtnText }}</button>
      <button @click="setCookies">Modify</button>
    </div>
  </div>
  <div class="container" style="background-color: #161A30;" v-else>
    <h1 class="loader">
      <span>L</span>
      <span>O</span>
      <span>A</span>
      <span>D</span>
      <span>I</span>
      <span>N</span>
      <span>G</span>
    </h1>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
.container1 {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 150px 1fr 120px;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  /* justify-content: center; */
  /* padding: 50px; */
  align-items: center;
  background-color: #161A30;
  color: #B6BBC4;
}
.top {
  backdrop-filter: blur(5px);
  width: 100vw;
  height: 100%;
  /* border-radius: 8px; */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 2px;
}
table {
  background-color: var(--var-dark);
}
tr,
th {
  background: var(--var-light);
  width: 50px;
  padding: 5px;
  color: #161A30;
}
td {
  padding: 5px;
}
td input {
  height: 35px;
  width: 200px;
  border: 1px var(--var-dark) solid;
  border-radius: 15px;
  padding: 5px;
}
.options {
  background: #222831;
  width: 100vw;
  height: 100%;
  padding: 5px;
  display: flex;
  justify-content: center;
  align-items: center;
  /* border-radius: 8px; */
  gap: 10px;
}
.options > button {
  flex-basis: 20%;
  height: 50px;
  border: 1px #ffc470 solid;
  border-radius: 15px;
  background: #F0ECE5;
}
.options > button:hover {
  background: var(--var-mid);
}

input:hover, input:focus{
  background-color: var(--var-mid);
  color: white
}

h1.loader {
  text-align: center;
  text-transform: uppercase;
  font-family: 'Nunito', sans-serif;
  font-size: 4.6875em;
  color: transparent;
  letter-spacing: 0.01em;
}

.loader span {
  text-shadow:
    0 0 2px rgba(204, 208, 212,0.9),
    0 15px 25px rgba(0, 0, 0, 0.3),
    0 -2px 3px rgba(0, 0, 0, 0.1),
    0 -5px 10px rgba(255, 255, 255, 0.5),
    0 5px 10px rgba(0, 0, 0, 0.3),
    0 3px 4px rgba(255, 255, 255, 0.2),
    0 0 20px rgba(255, 255, 255, 0.45);
  
    animation: loading 0.85s ease-in-out infinite alternate;
}

@keyframes loading {
	to {text-shadow:
    0 0 2px rgba(204, 208, 212,0.2),
    0 0 3px rgba(0, 0, 0, 0.02),
    0 0 0 rgba(0, 0, 0, 0),
    0 0 0 rgba(255, 255, 255, 0),
    0 0 0 rgba(0, 0, 0, 0),
    0 0 0 rgba(255, 255, 255, 0),
    0 0 0 rgba(255, 255, 255, 0);}
}

.loader span:nth-child(2) {
  animation-delay:0.15s;
}

.loader span:nth-child(3) {
  animation-delay:0.30s;
}

.loader span:nth-child(4) {
  animation-delay:0.45s;
}

.loader span:nth-child(5) {
  animation-delay:0.60s;
}

.loader span:nth-child(6) {
  animation-delay:0.75s;
}

.loader span:nth-child(7) {
  animation-delay:0.90s;
}
</style>

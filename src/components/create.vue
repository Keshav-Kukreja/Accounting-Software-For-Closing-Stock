<script>
import { ref,onMounted } from "vue";
import { useRouter } from 'vue-router'

export default {
  setup() {
    const url="http://127.0.0.1:5000"
    const router = useRouter();
    const Discription = ref("");
    const discriptionList = ref([]);
    const ready = ref(false);

    const data = ref({
      code: "",
      name: "",
      fy: [],
      Discription: {},
      total: { Tax: "Total", OS: 0, Pur: 0, GP: 0, Sale: 0, CS: 0 },
    });

    const fy = ref("");
    const addDiscription = () => {
      if (Discription.value.trim() !== "" && !discriptionList.value.includes(Discription.value)) {
        discriptionList.value.push(Discription.value);
        Discription.value = "";
      }
      else {
        alert("Discription already exists")
        Discription.value = "";
      }
    };

    const code = () => {
      fetch(`${url}/new_code`)
        .then((response) => {
          if (!response.ok) {
            console.error("Error fetching data:", response.statusText);
          }
          return response.json();
        })
        .then((res) => {
          console.log(res);
           if (res.length === 1) {
             data.value.code = parseInt(res[0]["CODE"]) + 1;
             ready.value = true;
           }
           else{
             data.value.code = 1;
             ready.value = true;
           }
        });
    };

    const deleteDiscription = (i) => {
      discriptionList.value = discriptionList.value.filter((d) => d !== i);
    };

    const dataFetch = () => {
      if (discriptionList.value.length > 0  && fy.value !== "" && data.value.name !== "") {
        data.value.fy.push(parseInt(fy.value));
        let i = 0;
        while (i < discriptionList.value.length) {
          data.value.Discription[i] = {
            Tax: discriptionList.value[i],
            OS: 0,
            Pur: 0,
            GP: 0,
            Sale: 0,
            CS: 0,
          };
          i++;
        }
        fetch(`${url}/create`, {
          method: "POST",
          body: JSON.stringify(data.value), // Note the .value, as data is a ref
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((res) => {
            return res.json();
          })
          .then((data) => {
            console.log(data);
            alert(data);
            // window.location.reload();
            router.go(-1);
          });
      } else {
        alert("You need to fill all the fields");
      }
    };

    onMounted(() => {
      code();
    });


    return {
      Discription,
      discriptionList,
      addDiscription,
      deleteDiscription,
      dataFetch,
      fy,
      data,
      code,
      ready,
    };
  },
};
</script>

<template>
  <div class="container createContainer">
      <div id="details">
        <input v-if="!ready"
          type="text"
          id="code-input"
          value="Loading..."
          disabled
        />
        <input v-else
          type="text"
          id="code-input"
          :value="data.code"
          disabled
        />
        <input
          type="text"
          placeholder="Company Name"
          id="name-input"
          v-model="data.name"
          style="width: 420px;"
        />
        <input
          type="text"
          placeholder="F.Y. : 2021"
          id="fy-input"
          v-model="fy"
        />
      </div>
      <div id="add">
        <input type="text" placeholder="Discriptions" v-model="Discription" />
        <button @click="addDiscription">Add</button>
      </div>
      <h2 id="heading">Discriptions</h2>
      <div id="discriptions">
        <div class="items" v-for="i in discriptionList" :key="i">
          <div class="disc_name">{{ i }}</div>
          <button @click="deleteDiscription(i)" class="delete">Remove</button>
        </div>
      </div>
      <div id="bottom">
        <button @click="dataFetch">Save</button>
        <button @click="$router.go(-1)">Cancel</button>
      </div>
  </div>
</template>

<style>
:root {
  --var-radius: 8px;
}
.createContainer {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 100px 50px 50px 1fr 60px;
  place-items: center;
}

#top-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 800px;
  height: 600px;
  border-radius: 15px;
  background: var(--var-mid);
}

#details {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 5px;
  width: 100%;
  height: 100%;
  padding: 10px;
  background: var(--var-blue);
}

#details > input {
  border-radius: var(--var-radius);
  border: 1px solid var(--var-mid);
  text-align: center;
  height: 35px;
  width: 100px;
}


#add {
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin-top: 5px;
  width: 100%;
  height: 100%;
  padding: 10px;
  background: var(--var-blue);
}

#add > input,
#add > button {
  padding: 5px;
  border-radius: var(--var-radius);
  border: 1px solid var(--var-mid);
  text-align: center;
  flex-basis: 20%;
}

#heading {
  margin-top: 5px;
  text-align: center;
  padding: 5px;
  background-color: var(--var-blue);
  width: 100%;
  height: 100%;
}

#discriptions {
  width: 100%;
  height: 100%;
  overflow-y: scroll;
  background-color: white;
  text-align: center;
  margin-top: 1px;
  display: flex;
  align-items: center;
  flex-direction: column;
  gap: 2px;
  scrollbar-color: white var(--var-blue);
}

.items {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 5px;
  border-radius: var(--var-radius);
  width: 50%;
  height: 50px;
  gap: 5px;
}
.disc_name {
  display: flex;
  color: white;
  justify-content: center;
  align-items: center;
  background-color: var(--var-mid); 
  flex-basis: 70%; 
  height: 40px;
  border-radius: 15px;
  font-size: 16pt
}
.delete {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--var-blue);
  border-radius: 20px;
  border: 1px solid var(--var-blue) solid;
  flex-basis: 25%;
  height: 40px;
  font-size: 12pt
}
.delete:hover {
  background-color: red;
}

button:hover {
  background-color: var(--var-mid);
  color: white;
}

#discriptions:hover {
  overflow-y: scroll;
  scrollbar-color: var(--var-mid) var(--var-blue);
}

#bottom {
  display: flex;
  margin: 5px;
  width: 100%;
  height: 100%;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background-color: var(--var-mid);
}

#bottom > button {
  width: 30%;
  height: 45px;
  border: 1px solid var(--var-blue);
  border-radius: var(--var-radius);
  background: var(--var-light);
}
 #bottom > button:hover {
  background-color: var(--var-blue);
  color: green;
 }
</style>

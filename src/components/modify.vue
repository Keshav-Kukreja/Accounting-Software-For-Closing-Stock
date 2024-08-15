<template>
  <div :class="$style.container">
    <div :id="$style.header">
      <h1>Modify</h1>
    </div>
    <div :id="$style.configSection">
      <button
        style="
          width: 100px;
          height: 35px;
          background: red;
          border-radius: 8px;
          border: 1px solid white;
        "
        @click="$router.go(-1)"
      >
        Back
      </button>
      <input
        type="text"
        placeholder="Company Name"
        id="code-input"
        v-model="storeData.name"
        style="
          width: 420px;
          height: 35px;
          text-align: center;
          border-radius: 8px;
          border: 1px solid black;
        "
      />
      <input
        type="text"
        placeholder="F.Y. : 2021"
        id="fy-input"
        v-model="storeData.fy"
        style="
          width: 150px;
          height: 35px;
          border-radius: 8px;
          border: 1px solid black;
          text-align: center;
        "
        readonly
      />
      <button
        style="
          width: 100px;
          height: 35px;
          background: green;
          border-radius: 8px;
          border: 1px solid white;
        "
        @click="PostData"
      >
        Save
      </button>
    </div>
    <div :id="$style.addDiscription">
      <input
        type="text"
        placeholder="Discription Name"
        style="
          width: 250px;
          height: 35px;
          border-radius: 8px;
          border: 1px solid black;
          text-align: center;
        "
        v-model="newDiscription"
      />
      <button
        style="
          width: 100px;
          height: 35px;
          background: red;
          border-radius: 8px;
          border: 1px solid white;
        "
        @click="addDiscription"
      >
        Add
      </button>
    </div>
    <div :id="$style.discriptionSection">
      <h2>Discriptions</h2>
      <div class="items" v-for="(i, index) in storeData.Discription" :key="i">
        <input
          class="disc_name"
          style="
            background: white;
            border: 1px solid black;
            text-align: center;
            color: black;
          "
          v-model="i.Tax"
        />
        <button @click="removeDescription(index)" class="delete">Remove</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  setup() {
    const url = "http://127.0.0.1:5000";

    const storeData = ref({});
    const PostData = () => {
      // fetch("${url}/modify", {
      //   method: "POST",
      //   headers: {
      //     "Content-Type": "application/json",
      //   },
      //   body: JSON.stringify(val),
      // })
      //   .then((res) => {
      //     return res.json();
      //   })
      //   .then((data) => {
      //     console.log(data.Post);
      //   });
      fetch(`${url}/modify`, {
        method: "POST",
        body: JSON.stringify({
          company: {
            code: $cookies.get("code").code,
            fy: $cookies.get("code").fy,
          },
          Data: storeData.value,
        }), // Note the .value, as data is a ref
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
    const getData = (code, fy) => {
      console.log(code, fy);
      fetch(`${url}/modify?code=${code}&fy=${fy}`)
        .then((res) => {
          return res.json();
        })
        .then((data) => {
          console.log(data);
          storeData.value = data;
        });
    };

    const newDiscription = ref("");

    const reorderedObj = () => {
      let reorderedObject = {};
      let newIndex = 0;
      for (const key in storeData.value.Discription) {
        reorderedObject[newIndex] = storeData.value.Discription[key];
        newIndex++;
      }
      storeData.value.Discription = reorderedObject;
      console.log(storeData.value);
    };

    const removeDescription = (index) => {
      delete storeData.value.Discription[index];
      reorderedObj();
    };

    const addDiscription = () => {
      const lastKey = Object.keys(storeData.value.Discription)[
        Object.keys(storeData.value.Discription).length - 1
      ];
      storeData.value.Discription[`${parseInt(lastKey) + 1}`] = {
        Tax: newDiscription.value,
        OS: 0,
        Pur: 0,
        GP: 0,
        Sale: 0,
        CS: 0,
      };
      console.log(storeData.value);
    };

    onMounted(() => {
      getData($cookies.get("code").code, $cookies.get("code").fy);
    });

    return {
      PostData,
      getData,
      storeData,
      removeDescription,
      newDiscription,
      addDiscription,
      reorderedObj,
      url,
    };
  },
};
</script>

<style module>
.container {
  width: 100vw;
  height: 100vh;
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 50px 80px 50px 1fr;
}

#header {
  grid-column-start: 1;
  grid-column-end: 2;
  grid-row-start: 1;
  grid-row-end: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffc470;
}

#configSection {
  grid-column-start: 1;
  grid-column-end: 2;
  grid-row-start: 2;
  grid-row-end: 2;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  background-color: #ffc470;
}
#discriptionSection {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100%;
  grid-column-start: 1;
  grid-column-end: 2;
  grid-row-start: 4;
  grid-row-end: 4;
  background-color: #ffc470;
  overflow: auto;
}

#discriptionSection > table {
  width: 100%;
  height: 100%;
}

#addDiscription {
  grid-column-start: 1;
  grid-column-end: 2;
  grid-row-start: 3;
  grid-row-end: 3;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffc470;
}
</style>

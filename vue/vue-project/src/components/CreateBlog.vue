<template>
    <div class="flex  justify-evenly">
        <img src="/public/add.jpg" alt="" class=" mt-40 ml-40">
        <form @submit.prevent="addBlog" class="bg-white border-2 border-green-600 w-4/12 h-2/3 ml-1/2 mt-60 px-10 py-8 text-left shadow-md rounded-lg">
            <div>
                <div>
                    <label class="block text-lg font-medium text-black mb-1">Title</label>
                    <input type="text" v-model="blog.title" class="shadow-md w-full h-10 px-5 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5">
                </div>
                <div>
                    <label for="" class="block text-lg font-medium text-black mb-1">Description</label>
                    <textarea name="description" v-model="blog.description" class="shadow-md w-full h-40 px-5 px-2 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5"></textarea>
                </div>
                <div class="flex justify-evenly">
                    <button class="rounded-lg ring-2 ring-lime-500 py-2 px-5 mt-6">Add Post</button>
                    <button class="rounded-lg ring-2 ring-red-500 py-2 px-5 mt-6" @click="cancelCreate">Cancel</button>
                </div>
            </div>
        </form>
    </div>
</template>
<script setup>
import axios from 'axios';
import {ref} from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from "vue-toastification";
const toast=useToast({ position: 'bottom-left'});
const router = useRouter();
const blog=ref({
    title:'',
    description:''
});
const addBlog = () => {
  axios.post(`http://127.0.0.1:8000/blogposts/`, {

    title:blog.value.title,
    description:blog.value.description
  } , {    withCredentials: true} )
  .then(response => {
    router.push({ name: 'Dashboard' });
    toast.success("Blog created successfully");
  })
  .catch(error => {
    console.error(error);
    toast.success("Blog created unsuccessfull");
  });
};

const cancelCreate=()=>{
    router.push({name:'Dashboard'});
    toast.error("Blog creation cancelled",{ position: 'bottom-right'});
  }

</script>
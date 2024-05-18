<template>
    <div>
      <nav class="bg-emerald-600">
        <div class="flex justify-evenly items-center  px-4 py-4">
          <div class="flex">
            <button class="text-white text-xl mx-20" @click="getMyPost"> My Posts</button>
            <button class="text-white text-xl mx-20" @click="getPost" >Explore</button>
            <button class="text-white text-xl mx-20" @click="createBlog" >Create Blog</button>
            <button>Logout</button>
            <!-- <router-link to="/dashboard" class="text-white text-xl mx-20">My posts</router-link>
            <router-link to="/allblogs" class="text-white text-xl mx-20">Explore</router-link>
            <router-link to="/blog-create" class="text-white  text-xl mx-20">Create blog</router-link>
            <router-link to="/" class="text-white  text-xl mx-20">Logout</router-link> -->
          </div>
        </div>
      </nav>
      <div class="container mx-auto px-4 py-4 mt-14">
        <div class="grid grid-cols-1 gap-4 "> 
          <div v-for="blog in blogs">
            <div class="bg-white border border-green-400 shadow-md rounded-lg p-6">
              <h2 class="text-5xl text-green-400 mb-5">{{ blog.title }}</h2> 
              <p class="text-gray-600 mb-4 text-xl">{{ blog.description }}</p> 
              <p class="text-gray-700 font-bold">Author: {{ blog.author }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from "vue-toastification";

const toast=useToast({ position: 'bottom-left'});
const blogs = ref([]);
const router = useRouter();
const getPost = () => {

     axios("http://127.0.0.1:8000/blogposts/?all=True",{
      method:"get",
      withCredentials: true
    })
        .then(response => {
            blogs.value = response.data;
            console.log(response.data)
        })
        .catch(error => {
            console.error(error);
            toast.error("Failed to fetch the data",{ position: 'bottom-right'});
        });
   
};
const getMyPost =()=>{
  router.push({name:'Dashboard'});
};
const createBlog = ()=>{
  router.push({name:'CreateBlog'});

};
// const post = () => {
//   axios("http://localhost:8000/blogposts/?all=True",{method: "get", withCredentials: true}).then((response) => { console.log(response)})
// // }
// onMounted(post) 
</script>
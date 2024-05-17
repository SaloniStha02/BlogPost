<template>
    <div>
      <nav class="bg-emerald-600">
        <div class="flex justify-evenly items-center px-4 py-4">
          <div class="flex">
            <router-link to="/dashboard" class="text-white text-xl mx-20">My posts</router-link>
            <router-link to="/allblogs" class="text-white text-xl mx-20">Explore</router-link>
            <router-link to="/blog-create" class="text-white  text-xl mx-20">Create blog</router-link>
            <router-link to="/" class="text-white  text-xl mx-20">Logout</router-link>
          </div>
        </div>
      </nav>
      <div class="container mx-auto px-4 py-4 mt-14">
        <div class="grid grid-cols-1 gap-4"> 
            <div class="bg-white border border-green-400 shadow-md rounded-lg p-6" v-for="blog in blogs">
              <h2 class="text-5xl text-green-400 mb-5">{{ blog.title }}</h2> 
              <p class="text-gray-600 mb-4 text-xl">{{ blog.description }}</p> 
              <div class="flex flex-row-reverse">
                <button class="ring-2 ring-red-600 rounded-lg text-xl py-2 px-5">Delete</button>
                <button class="ring-2 ring-green-600 rounded-lg mr-11 text-xl py-2 px-5" @click="updatePost">Update</button>
              </div>
          
            </div>
        </div>
      </div>
    </div>
  </template>
<script setup>
import axios from 'axios';
import {ref} from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from "vue-toastification";

const toast=useToast({ position: 'bottom-left'});
const blogs = ref([]);
const router = useRouter();
const getMyPost = () => {

     axios("http://127.0.0.1:8000/blogposts/",{
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
const getPost=()=>{
  router.push({name:'AllBlogs'});
};
const createBlog=()=>{
  router.push({name:'CreateBlog'});
};
const updatePost=()=>{
      router.push({name:'UpdateBlog'});
  }

</script>
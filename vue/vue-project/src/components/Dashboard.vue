<template>
  <div>
    <nav class="bg-emerald-600">
      <div class="flex justify-evenly items-center px-4 py-4">
        <div class="flex">
          <button class="text-white text-xl mx-20" @click="getMyPost">My Posts</button>
          <button  class="text-white text-xl mx-20" @click="getPost">Explore</button>
          <button class="text-white text-xl mx-20" @click="createBlog">Create Blog</button>
          <button  @click="logOut"class="text-white text-xl mx-20" >Logout</button>
        </div>
      </div>
    </nav>
    <div class="container mx-auto px-4 py-4 mt-14">
      <div class="grid grid-cols-1 gap-4"> 
          <div class="bg-white border border-green-400 shadow-md rounded-lg p-6" v-for="blog in blogs">
            <h2 class="text-5xl text-green-400 mb-5">{{ blog.title }}</h2> 
            <p class="text-gray-600 mb-4 text-xl">{{ blog.description }}</p> 
            <div class="flex flex-row-reverse">
              <button class="ring-2 ring-red-600 rounded-lg text-xl py-2 px-5" @click="deleteBlog(blog.id)">Delete</button>
              <button class="ring-2 ring-green-600 rounded-lg mr-11 text-xl py-2 px-5" @click="updatePost(blog.id)">Update</button>
            </div>
          </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import axios from 'axios';
import {onMounted, ref} from 'vue';
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
const logOut=()=>{
  axios("http://127.0.0.1:8000/logout/",{
      method:"post",
      withCredentials: true
    })
        .then(response => {
            if (response.status === 200) {
                router.push({ path: '/' });
                toast.success("Logout Successful",{position:'bottom-right'});
            }
        })
        .catch(error => {
            console.error('Logout failed:', error);
            toast.error("Logout Unsuccessful",{position:"bottom-right"});
          
        });
}
const updatePost=(id)=>{
    router.push({name:'UpdateBlog',params: { blogId: id }});
}
const deleteBlog=(blogId)=>{
const confirmation = window.confirm("Are you sure you want to delete this blog?");
if(confirmation){
  axios.delete(`http://127.0.0.1:8000/blogpost-detail/${blogId}/`, {
  withCredentials: true
})
    .then(response => {
    
      console.log('Blog soft deleted successfully');
      toast.success("Blog deleted successfully",{ position: 'bottom-right'});
      blogs.value = blogs.value.filter(blog => blog.id !== blogId);
    })

    .catch(error => {
      console.error('Error soft deleting post', error);
      toast.error("Blog deletion unsuccessful",{ position: 'bottom-right'});

    });
}
else{
    console.error("Invalid Error");
    toast.error("Blog is not deleted",{position:'bottom-right'});
}
}
onMounted(getMyPost);
</script>
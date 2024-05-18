<template>
    <div class="flex  justify-evenly">
      <img src="/public/add.jpeg" alt="" class=" mt-40 ml-28">
      <form v-if="blog"  @submit.prevent="updBlog"class="bg-white border-2 border-green-600 w-4/12 h-2/3 ml-1/2 mt-52 px-10 py-8  mr-20 text-left shadow-md rounded-lg">
          <div>
              <div>
                  <label class="block text-lg font-medium text-black mb-1">ID</label>
                  <input type="number" name="blogId"class="shadow-md w-full h-10 px-5 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5" v-model="blog.id"disabled>
              </div>
              <div>
                  <label class="block text-lg font-medium text-black mb-1">Title</label>
                  <input type="text" name="title"class="shadow-md w-full h-10 px-5 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5" v-model="blog.title">
              </div>
              <div>
                  <label for="" class="block text-lg font-medium text-black mb-1">Description</label>
                  <textarea name="description" class="shadow-md w-full h-40 px-5 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5" v-model="blog.description"></textarea>
              </div>
              <div class="flex justify-evenly">
                  <button class="rounded-lg ring-2 ring-lime-500 py-2 px-5 mt-6">Update</button>
                  <button class="rounded-lg ring-2 ring-red-500 py-2 px-5 mt-6" @click="cancelUpdate">Cancel</button>
              </div>
          </div>
      </form>
  </div>
</template>
<script setup>
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useToast } from "vue-toastification";

const route = useRoute();
const toast = useToast({ position: 'bottom-left' });
const blogId = ref(route.params.blogId);
const blog = ref(null);
const router = useRouter();

const fetchBlog = () => {
axios.get(`http://127.0.0.1:8000/blogpost-detail/${blogId.value}/`, {
  withCredentials: true
})
.then(response => {
  const blogData = response.data;
  if (!blogData.is_deleted) {
    blog.value = blogData;
  } else {
    router.push('/dashboard');
    toast.error("Blog not found or has been deleted", { position: 'bottom-right' });
  }
})
.catch(error => {
  console.error(error);
});
};

const updBlog = () => {
if (!blog.value) {
  console.error("Blog data is undefined");
  return;
}
axios.patch(`http://127.0.0.1:8000/blogpost-detail/${blogId.value}/`, {
  title: blog.value.title,
  description: blog.value.description
}, {
  withCredentials: true
})
.then(response => {
  console.log('Blog Updated', response.data);
  router.push('/dashboard');
  toast.success("Blog edited successfully", { position: 'bottom-right' });
})
.catch(error => {
  console.error(error);
  toast.error('Failed to update blog data.');
});
};

const cancelUpdate = () => {
router.push({ name: 'Dashboard' });
toast.error("Cancelled Update", { position: 'bottom-right' });
};

onMounted(fetchBlog);
</script>
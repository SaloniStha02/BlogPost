<template>
      <div class="flex  justify-evenly">
        <img src="/public/add.jpeg" alt="" class=" mt-40 ml-28">
        <form action="" class="bg-white border-2 border-green-600 w-4/12 h-2/3 ml-1/2 mt-52 px-10 py-8  mr-20 text-left shadow-md rounded-lg">
            <div>
                <div>
                    <label class="block text-lg font-medium text-black mb-1">ID</label>
                    <input type="number" class="shadow-md w-full h-10 px-5 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5"disabled>
                </div>
                <div>
                    <label class="block text-lg font-medium text-black mb-1">Title</label>
                    <input type="text" class="shadow-md w-full h-10 px-5 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5">
                </div>
                <div>
                    <label for="" class="block text-lg font-medium text-black mb-1">Description</label>
                    <textarea name="description" class="shadow-md w-full h-40 px-5 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5" id=""></textarea>
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
import { useRouter } from 'vue-router';
import{ref } from 'vue';
import { useToast } from "vue-toastification";
const toast=useToast({ position: 'bottom-left'});
const router = useRouter();
const updBlog = ref({
    'title': ' ',
    'description':''
});
const cancelUpdate=()=>{
    router.push({name:'Dashboard'});
    toast.error("Cancelled Update",{ position: 'bottom-right'});
  }

</script>
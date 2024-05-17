<template>
    <div class="container2 flex flex-col md:flex-row items-center justify-center">
        <form class="bg-white border-2 border-green-500 w-56 mt-20 ml-60 md:w-96 py-12 px-16 md:px-8 rounded-lg shadow-md text-left" @submit.prevent="login()">  
            <label class="mt-5 ml-1 block tracking-wide text-lg text-black mb-1 md:mb-5">Email:</label>
            <input type="email" id="email" class="shadow-md w-full h-12 px-5 py-2 border-2 border-black-300 rounded-lg text-lg mb-5" v-model="user_data.email" required>
            <label class="mt-5 ml-1 block tracking-wide text-lg text-black mb-1 md:mb-5">Password:</label>
            <input type="password" class="shadow-md w-full h-12 px-5 py-2 border-2 border-black-500 rounded-lg text-lg mb-5" v-model="user_data.password" required> 
            <button class=" bg-green-600 rounded-lg px-4 py-2 ml-16 my-10 md:my-10 md:w-48 text-white text-lg mx-auto" type="submit">Sign-in</button>  
            <p class="text-base ml-14 md:ml-15">Don't have an account?<router-link to="/createuser">Sign up</router-link></p>
        </form>
        <img src="/login.jpeg" alt="" class="ml-40 mt-20">
    </div>
</template>
<script setup>
import { ref } from 'vue'; 
import { useRouter } from 'vue-router'; 
import axios from 'axios';
import { useToast } from "vue-toastification";

const toast=useToast({ position: 'bottom-left'});
const router = useRouter();
const user_data=ref({
  email:'',
  password:'',
})

const login = () => {
    axios.post('http://127.0.0.1:8000/login/', {
        email: user_data.value.email, 
        password: user_data.value.password},
        {withCredentials: true})
    .then(response => {
      router.push({ name: 'Dashboard' });
      toast.success("Login Successful!!",{position:'bottom-right'});

    })
    .catch(error => {
        console.error('Login failed:', error.message);
        toast.error("Login Unsuccessful!!",{position:'bottom-right'});
    });
};
</script>
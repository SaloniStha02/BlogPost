<template>
        <div class=" flex flex-col md:flex-row  items-center justify-around">
        <div><img src="/public/register.jpeg" alt="" class="mt-32"></div>
     <form @submit.prevent="addAuthor" class="bg-white border-2 border-green-600 w-6/12 h-4/5 mt-28 px-10 py-8 text-left shadow-md rounded-lg ">
         <div class="grid grid-cols-2  gap-5">
             <div >
                 <label class="block text-lg font-medium text-black mb-1">First Name:</label>
                 <input type="text" name="fname" id="fname" class="shadow-md w-full h-10 px-5 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5" v-model="user.first_name" required>
             </div>
             <div>
                 <label class="block text-lg font-medium text-black mb-1">Last Name:</label>
                 <input type="text" name="lname" id="lname"class="shadow-md w-full h-10 px-5 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5"  v-model="user.last_name" required>
             </div>
             <div>
                 <label class="block text-lg font-medium text-black mb-1">Email:</label>
                 <input type="email" name="email" id="email"class="shadow-md w-full h-10 px-5 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5"  v-model="user.email" required>
             </div>
             <div >
                 <label class="block text-lg font-medium text-black mb-1">Password:</label>
                 <input type="password" name="password" id="password"class="shadow-md w-full h-10 px-5 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5"  v-model="user.password" required>
                 <span v-if="passwordWarning !== ''" class="warning">{{ passwordWarning }}</span>
             </div>
             <div >
                 <label class="block text-lg font-medium text-black mb-1">Confirm Password:</label>
                 <input type="password" name="confpassword" id="cpassword" class="shadow-md w-full h-10 px-5 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5" v-model="confirmPassword">
             </div>
        
   
             <div >
                 <label class="block text-lg font-medium text-black mb-1">Address:</label>
                 <input type="text" name="address" id="address" class="shadow-md w-full h-10 px-5 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5" v-model="user.address">
             </div>
      
             <div >
                 <label class="block text-lg font-medium text-black mb-1">Phone number:</label>
                 <input type="number" name="phone_no" id="phone_no"class="shadow-md w-full h-10 px-5 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5"  v-model="user.phone_no" maxlength="10" minlength="10">
                 <span v-if="!isValidPhone" class="warning">{{ phoneWarning }}</span>
             </div>
             <div >
                 <label class="block text-lg font-medium text-black mb-1">Age:</label>
                 <input type="number" name="age" id="age" class="shadow-md w-full h-10 px-5 py-2 border-2 border-gray-300 rounded-lg text-lg mb-5" v-model="user.age">
             </div>
         </div>
         <div class="flex justify-center">
                <button type="submit" class=" bg-green-600 rounded-lg px-4 py-2 text-white mr-12 mt-6">Sign-up</button>
                <button @click="backSign" class="bg-red-600 rounded-lg px-4 py-2 text-white mt-6 ">Cancel</button>
        </div>
     </form>
 </div>
 </template>
 
 <script setup>
 import axios from 'axios';
 import { useRouter } from 'vue-router';
 import { ref } from 'vue';
 import { useToast } from "vue-toastification";
 
 const toast=useToast();
 const url = "http://127.0.0.1:8000/users/";
 const user = ref({
     email: '',
     password: '',
     first_name: '',
     last_name: '',
     address: '',
     phone_no: '',
     age: ''
 });
 
 const router = useRouter();
 const confirmPassword = ref('');
const passwordWarning = ref('');
const isValidPhone = ref(true);
const phoneWarning = ref ('');
const backSign=()=>{
      router.push({name:'Login'});
      toast.error("Cancelled Sign up",{ position: 'bottom-right'});
  }
 const addAuthor = () => {

     passwordWarning.value = '';
     isValidPhone.value = true;
     phoneWarning.value = '';

     const passwordReg = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9]).{8,}$/;
     if (!passwordReg.test(user.value.password)) {
         passwordWarning.value = "Must contain at least one uppercase letter, one lowercase letter, one special character, one number, and should be at least 8 characters long.";
     }
 
   
     if (user.value.password !== confirmPassword.value) {
         passwordWarning.value = "Passwords do not match";
     }
 
     const phoneNumber = user.value.phone_no.toString(); 
     if(phoneNumber.length !== 10) {
         isValidPhone.value = false;
         phoneWarning.value = "Please enter a valid 10-digit phone number";
     }
 
     if ( passwordWarning.value !== '' || !isValidPhone.value) {
         return;
     }
     axios.post(url,{
         email:user.value.email,
         password:user.value.password,
         first_name:user.value.first_name,
         last_name:user.value.last_name,
         address:user.value.address,
         phone_no:user.value.phone_no,
         age:user.value.age
     })
         .then(response => {
             router.push({ name: 'Login' });
             toast.success("User added successfully");
         })
         .catch(error => {
             console.error(error);
             toast.error("User added unsuccessful");
         });
 };
 </script>
 
 <style>
 </style>
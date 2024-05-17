import{createWebHistory,createRouter} from 'vue-router';
import Form from './components/Form.vue';
import ReadUser from './components/ReadUser.vue';
import EditUser from './components/EditUser.vue';
import Login from './components/Login.vue';
import Signup from './components/Signup.vue';
import Dashboard from './components/Dashboard.vue';
import AllBlogs from './components/AllBlogs.vue';
import CreateBlog from './components/CreateBlog.vue';
import UpdateBlog from './components/UpdateBlog.vue';
const routes=[
{
    name:'ReadUser',
    path :'/display-user',
    component:ReadUser
    
},
{
    name:'Form',
    path :'/createuser',
    component: Form
    
},
{
    name:'EditUser',
    path :'/edituser/:userId',
    component: EditUser,
    props:true
    
},
{
    name:'Login',
    path :'/',
    component: Login
},
{
    name:'Signup',
    path :'/signup',
    component: Signup
},
{
    name:'Dashboard',
    path:'/dashboard',
    component:Dashboard
},
{
    name:'AllBlogs',
    path:'/allblogs',
    component:AllBlogs
},
{
    name:'CreateBlog',
    path:'/blog-create',
    component:CreateBlog
},
{
    name:'UpdateBlog',
    path:'/blog-update',
    component:UpdateBlog
},
];

const router=createRouter({
    history:createWebHistory(),
    routes
});
export default router;


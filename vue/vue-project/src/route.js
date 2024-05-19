import{createWebHistory,createRouter} from 'vue-router';
import Form from './components/Form.vue';
import Login from './components/Login.vue';
import Dashboard from './components/Dashboard.vue';
import AllBlogs from './components/AllBlogs.vue';
import CreateBlog from './components/CreateBlog.vue';
import UpdateBlog from './components/UpdateBlog.vue';
const routes=[

{
    name:'Form',
    path :'/createuser',
    component: Form,
    meta: {
      requiresAuth: false,
    },
    
},
{
    name:'Login',
    path :'/',
    component: Login,
    meta: {
      requiresAuth:false,
    },
},
{
    name:'Dashboard',
    path:'/dashboard',
    component:Dashboard,
    meta: {
      requiresAuth: true,
    },
},
{
    name:'AllBlogs',
    path:'/allblogs',
    component:AllBlogs,
    meta: {
      requiresAuth: true,
    },
},
{
    name:'CreateBlog',
    path:'/blog-create',
    component:CreateBlog,
    meta: {
      requiresAuth: true,
    },
},
{
    name:'UpdateBlog',
    path:'/blog-update/:blogId',
    component:UpdateBlog,
    meta: {
      requiresAuth: true,
    },
},
];

const router=createRouter({
    history:createWebHistory(),
    routes
});
function isAuthenticated() {
    const token = getJwtToken();
    return !!token;
  }
  
  function getJwtToken() {
    const tokenCookie = document.cookie.split(';').find(cookie => cookie.trim().startsWith('access_token='));
    if (tokenCookie) {
      return tokenCookie.split('=')[1]; 
    }
    return null;
  }
  
  router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
      if (isAuthenticated()) {
        next();
      } else {
        next('/');
      }
    } else {
      next();
    }
  });
  
export default router;


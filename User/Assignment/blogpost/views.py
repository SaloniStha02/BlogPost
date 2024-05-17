from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import BlogPost
from .models import NewUser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
import json,jwt,datetime,math,time
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError
from rest_framework.exceptions import AuthenticationFailed



class BlogView:
    @staticmethod
    @csrf_exempt
    def blog_list(request:HttpRequest):
        token=TokenRegeneration.check(request)
        print(token)
        if token:
            if request.method=='GET':
                    if 'all' in request.GET and request.GET['all'].lower() == 'true':
                        blogs=BlogPost.objects.filter(is_deleted=False)
                    else:
                        refresh_token= request.COOKIES.get("refresh_token")
                        payload=jwt.decode(refresh_token,'secret',algorithms='HS256')
                        author_id = payload.get('id')
                        author = NewUser.objects.get(id=author_id)
                        blogs = BlogPost.objects.filter(is_deleted=False, author=author)
                    print(blogs)
                    blog_data = [{
                        'id': blog.id,
                        'title': blog.title, 
                        'description': blog.description,
                        'published_date':blog.published_date,
                        'author': blog.author.email 
                        } for blog in blogs]
                    print(blog_data)
                    return JsonResponse(blog_data, safe=False)
            
            elif request.method == 'POST':
                data = json.loads(request.body)
                refresh_token= request.COOKIES.get("refresh_token")
                payload=jwt.decode(refresh_token,'secret',algorithms='HS256')
                author_id = payload.get('id')
                author = get_object_or_404(NewUser, id=author_id)
                blog = BlogPost.objects.create(title=data['title'],description=data['description'],author=author)
                return JsonResponse({'id': blog.id,'title': blog.id, 'description':blog.description,'published_date':blog.published_date, 'author':author.email}, status=201)
            else:
                return JsonResponse({'error': 'Method Not Allowed'}, status=405)
        else:

            return JsonResponse({"check": True})

class BlogViewDetail:

    @csrf_exempt
    def blog_details(request:HttpRequest,pk):
        token=TokenRegeneration.check(request)
        if token:
            if request.method=='GET':
                blog = BlogPost.objects.get(id=pk)
                blog_data ={
                    'id': blog.id,
                    'title': blog.title, 
                    'description': blog.description,
                    'published_date':blog.published_date,
                    'author': blog.author.email
                    } 
                return JsonResponse(blog_data)
            elif request.method == 'PATCH':
                data = json.loads(request.body)
                try:
                    blog = BlogPost.objects.get(id=pk)
                    blog.title = data['title']
                    blog.description = data['description']
                    blog.save()
                    return JsonResponse({
                        'id': blog.id, 
                        'title': blog.title, 
                        'description': blog.description,
                        'published_date':blog.published_date,
                        'author': blog.author.email
                        })
                except BlogPost.DoesNotExist:
                    return JsonResponse({'error': ' Blog not found'}, status=404)
            elif request.method == 'DELETE':
                blog = BlogPost.objects.get(id=pk)
                blog.delete()
                return JsonResponse({'message':'Blog deleted'}, status=204)
            else:
                return JsonResponse({'error': 'Method Not Allowed'}, status=405)
        else:
                return JsonResponse({'error':'Not Authenticated'})
    
class BlogRestoreView:
    @csrf_exempt
    def blog_restore(request:HttpRequest,pk):
        token=TokenRegeneration.check(request)
        if token:
            if request.method=='POST':
                blog=BlogPost.objects.get(id=pk)
                blog.restore()
                return JsonResponse({'message':'Blog Restored'}, status=200)
            else:
                return JsonResponse({'error': 'Method Not Allowed'}, status=405)
        else:
                return JsonResponse({'error':'Not Authenticated'})
        
        
class BlogHardDeleteView:
    @csrf_exempt
    def blog_hard_delete(request:HttpRequest,pk):
        token=TokenRegeneration.check(request)
        if token:
            if request.method=='DELETE':
                blog=BlogPost.objects.get(pk=pk)
                blog.delete(hard_delete=True)
                return JsonResponse({'message':'Blog hard deleted'}, status=204)
        else:
                return JsonResponse({'error':'Not Authenticated'})
        
class TokenRegeneration:
    @csrf_exempt
    def check(request:HttpRequest):
        token =request.COOKIES.get("access_token")
        print("token generation",token)
        print("token generation",request.COOKIES)   
        if token:
            try:
                payload=jwt.decode(token,"secret",algorithms="HS256")
                user_id=payload.get('id')
                user=NewUser.objects.get(pk=user_id)
                res={
                        'message':"token Authorization",
                        'data':{
                            'id':user.id,
                            'first_name':user.first_name,
                            'last_name':user.last_name,
                            'email':user.email,
                            'phone_no':user.phone_no,
                            'address':user.address,
                            'age':user.age
                        }
                }
                return JsonResponse(res,status=200)
            except ExpiredSignatureError:
                response=TokenRegeneration.regenerate(request)
                return response
            except InvalidTokenError:
                    return JsonResponse({
                        'message':'token invalid',
                    })   
            
    def regenerate(request:HttpRequest):
        access_token= request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get('refresh_token')
        now = datetime.datetime.now()
        dt_now =int(now.timestamp())
        if not access_token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            access_payload=jwt.decode(access_token,'secret',algorithms='HS256')
        except jwt.ExpiredSignatureError:
            refresh_payload = jwt.decode(refresh_token,'secret',algorithms='HS256')
            if dt_now < refresh_payload['exp']:
                access_payload={
                    'type':'access',
                    'id':refresh_payload.get('id'),
                    'email':refresh_payload.get('email'),
                    'exp': math.floor(time.time())+600,
                    'iat':math.floor(time.time())
                }
                new_access_token = jwt.encode(access_payload,'secret',algorithm ='HS256')
                refresh_payload={
                    'type':'refresh',
                    'id':refresh_payload.get('id'),
                    'email':refresh_payload.get('email'),
                    'exp': math.floor(time.time())+3600,
                    'iat':math.floor(time.time())
                }
                new_refresh_token = jwt.encode(refresh_payload,'secret',algorithm ='HS256')
                response = JsonResponse({'message':'token regenerate','access token':new_access_token,'refresh token':new_refresh_token},status=204,safe=False)
                response.set_cookie('access_token',new_access_token, httponly=True)
                response.set_cookie('refresh_token',new_refresh_token, httponly=True)
                return response
            else:
                raise AuthenticationFailed('Expired Session')
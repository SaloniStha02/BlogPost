from django.shortcuts import render
from .models import NewUser
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from rest_framework.exceptions import AuthenticationFailed
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError
import json,jwt,datetime,math,time
    
class UserListView:
    @staticmethod
    @csrf_exempt
    def user_list(request: HttpRequest):
        if request.method == 'GET':
            users = NewUser.objects.filter(is_deleted=False)
            user_data = [{'id': user.id, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name, 'phone_no': user.phone_no, 'address': user.address, 'age': user.age} for user in users]
            return JsonResponse(user_data, safe=False)
        
        elif request.method == 'POST':
            data = json.loads(request.body)
            user = NewUser.objects.create_user(email=data['email'],first_name=data['first_name'], last_name=data['last_name'],phone_no=data['phone_no'],address=data['address'],age=data['age'],password=data['password'])
            return JsonResponse({'id': user.id,'email': user.email, 'first_name':user.first_name, 'last_name':user.last_name, 'phone_no':user.phone_no, 'address':user.address,'age':user.age,'password':user.password}, status=201)
        
        else:
            return JsonResponse({'error': 'Method Not Allowed'}, status=405)


class UserDetailView:
    @csrf_exempt
    def user_detail(request:HttpRequest, pk ):
        if request.method == 'GET':
            user = NewUser.objects.get(id=pk)
            user_data = {'id': user.id,'email': user.email, 'first_name':user.first_name, 'last_name':user.last_name, 'phone_no':user.phone_no, 'address':user.address,'age':user.age}
            return JsonResponse(user_data)
        
        elif request.method == 'PATCH':
            data = json.loads(request.body)
            try:
                user = NewUser.objects.get(id=pk)
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.phone_no = data['phone_no']
                user.address = data['address']
                user.email = data['email']
                user.age = data['age']
                user.save()
                return JsonResponse({'id': user.id, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name, 'phone_no': user.phone_no, 'address': user.address, 'age': user.age})
            except NewUser.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            
        elif request.method == 'DELETE':
            try:
                user = NewUser.objects.get(id=pk)
                user.soft_delete()
                return JsonResponse({}, status=204)
            except NewUser.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            
        else:
            return JsonResponse({'error': 'Method Not Allowed'}, status=405)
        
class UserLogin:
    @csrf_exempt

    def login(request:HttpRequest):

        if request.method=='POST':
            token =request.COOKIES.get("access_token")
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
                
            data = json.loads(request.body)
            email=data['email']
            password=data['password']
            user=NewUser.objects.filter(email=email).first()
            if user is None:
                raise AuthenticationFailed('User not found')
            if not user.check_password(password):
                raise AuthenticationFailed('Incorrect Password')
            response=UserLogin.token_Generate(request,user)
            return response
        

    def token_Generate(request,user):
        access_payload={
                    'type':'access_token',
                    'id':user.id,
                    'email':user.email,
                    'exp': math.floor(time.time())+600,
                    'iat':math.floor(time.time())
                }
        access_token=jwt.encode(access_payload,"secret",algorithm="HS256")
        refresh_payload={
                    'type':'refresh_token',
                    'id':user.id,
                    'email':user.email,
                    'exp': math.floor(time.time())+ 3600,
                    'iat':math.floor(time.time())
                }
        refresh_token=jwt.encode(refresh_payload,"secret",algorithm="HS256")
        response = JsonResponse({'message':'success','access_token':access_token,'refresh_token':refresh_token}, status=200)
        response.set_cookie('access_token',access_token)
        response.set_cookie('refresh_token',refresh_token)
        return response



class TokenRegeneration:
    @csrf_exempt
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
            

from rest_framework.decorators import api_view
# To return the Response in JSON format
from rest_framework.response import Response
# For Validation of Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .models import Group_Log, User_data 

from .serializers import RegisterSerializer
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from Crypto.Cipher import AES

# SSS
import random
from math import ceil
from decimal import Decimal

FIELD_SIZE =10**5


def reconstruct_secret(shares):
    sums = 0
    prod_arr = []
    
    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)

        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                prod *= Decimal(Decimal(xi)/(xi-xj))

        prod *= yj
        sums += Decimal(prod)

    return int(round(Decimal(sums), 0))


def polynom(x, coefficients):

    point = 0

    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        point += x ** coefficient_index * coefficient_value
    return point


def coeff(t, secret):
    coeff = [random.randrange(0, FIELD_SIZE) for _ in range(t - 1)]
    coeff.append(secret)
    return coeff


def generate_shares(n, m, secret):

    coefficients = coeff(m, secret)
    shares = []
    for i in range(1, n+1):
        x = random.randrange(1, FIELD_SIZE)
        shares.append((x, polynom(x, coefficients)))

    return shares

# AES Part
def aes_encrypt(password, plaintext):
    str_val = str(password)
    key = str_val.encode()
    cipher = AES.new(key, AES.MODE_EAX,nonce=b'1234567890123456')
    data = plaintext.encode()
    ciphertext = cipher.encrypt(data)
    print("Cipher text:", ciphertext)
    return ciphertext

def aes_decrypt(password, ciphertext):
    str_val = str(password)
    key = str_val.encode()
    print(type(key))
    cipher = AES.new(key, AES.MODE_EAX,nonce=b'1234567890123456')
    plaintext = cipher.decrypt(ciphertext)
    print("Plain text:", plaintext)
    # # type(plaintext.decode())
    # # print(codecs.decode(plaintext))
    # print




# Login Route
@api_view(['POST'])
def login(request):
    serializer = AuthTokenSerializer(data=request.data)
    # Raising expection if password or username is incorrect
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _,token = AuthToken.objects.create(user)
    
    return Response({
        'user_info':{
            'id':user.id,
            'username':user.username,
            'email':user.email,
        },
        
        'token': token})


# Register the User
@api_view(['POST'])
def register(request):
    data = json.loads(request.body)
    if(len(data['password'])<6):
        return(Response({'error':'Password should be atleast 6 characters'},status=400))
    serializer = RegisterSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    user_data = User_data(username=user.username)
    user_data.save()
    _,token = AuthToken.objects.create(user)
    return JsonResponse({
        'user_info':{
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
        },
        'token':token
    },safe=False)

@api_view(['GET'])
def get_user(request):
    user = request.user
    if(user.is_authenticated):
        return Response({
            'user_info':{
                'id':user.id,
                'username':user.username,
                'email':user.email,
                'first_name':user.first_name,
                'last_name':user.last_name,
        }
    })
    
    return Response({'error':'User is not authenticated'},status=400)


@api_view(['POST'])
def create_group(request):
    user = request.user
    if(user.is_authenticated):
        user_data = User_data.objects.get(username=user.username)
        total_group_users = request.data['group_members']
        total_group_users.append(user.username)
        log =Group_Log(group_name=request.data['group_name'],group_members={"group_members":total_group_users})
        log.save()
        for i in (total_group_users):
            user_data = User_data.objects.get(username=i)
            user_data.groups['groups'].append({
            'group_name':request.data['group_name'],
            'group_members':total_group_users,
            })
            user_data.save()
        return Response({
                'group_details':user_data.groups
            })
    return(Response({'error':'User is not authenticated'},status=400))

# Groups
@api_view(['GET'])
def get_group_activity(request):
    user = request.user
    if(user.is_authenticated):
        user_data = User_data.objects.get(username=user.username)
        group_data = user_data.groups['groups']
        return Response({
                'groups':group_data
            })
    return(Response({'error':'User is not authenticated'},status=400))

# Generating Shares for the Group and Posting the each user's Shares in their User DATA
@api_view(['POST'])
def post_data_for_sss(request):
    user = request.user
    if(user.is_authenticated):
        user_data = User_data.objects.get(username=user.username)
        group_data = Group_Log.objects.get(group_name=request.data['group_name'])
        imgurl = group_data.image.url
        n = len(group_data.group_members['group_members'])
        k = request.data['members_required']
        secret = request.data['secret']
        shares = generate_shares(n, k, secret)
        group_data.image_url=aes_encrypt(secret,imgurl)
        group_data.members_required = k
        group_data.combined_shares = {"combined_shares":[]}
        group_data.save()
        for i in range(0,len(group_data.group_members['group_members'])):
            user_data = User_data.objects.get(username=group_data.group_members['group_members'][i])
            user_data.current_shares['shares'] = [{
                'group_name':request.data['group_name'],
                'shares':shares[i]
            }]
            user_data.save()
        return Response({
                'shares':shares
        })
    return(Response({'error':'User is not authenticated'},status=400))

# Commiting the Share to the Group
@api_view(['POST'])
def commit_share(request):
    user = request.user
    if(user.is_authenticated):
        user_data = User_data.objects.get(username=user.username)
        group_data = Group_Log.objects.get(group_name=request.data['group_name'])
        for i in range(0,len(user_data.current_shares['shares'])):
            if(user_data.current_shares['shares'][i]['group_name']==request.data['group_name']):
                user_commited_share=user_data.current_shares['shares'][i]['shares']
                group_data.combined_shares['combined_shares'].append(user_commited_share)
                group_data.save()
                return Response({
                    'message':'Share Committed',
                    'group_data':group_data.combined_shares
                })
        return Response({
                'error':'No Shares Found'
        })
    return(Response({'error':'User is not authenticated'},status=400))


@api_view(['POST'])
def get_secret(request):
    user = request.user
    if(user.is_authenticated):
        user_data = User_data.objects.get(username=user.username)
        group_data = Group_Log.objects.get(group_name=request.data['group_name'])
        if(len(group_data.combined_shares['combined_shares'])>=group_data.members_required):
            print(group_data.combined_shares['combined_shares'])
            secret = reconstruct_secret(group_data.combined_shares['combined_shares'])
            return Response({
                'secret':secret
            })
        return Response({
                'error':'Not Enough Shares'
        })
    return(Response({'error':'User is not authenticated'},status=400))

@api_view(['POST'])
def get_image_url(request):
    user = request.user
    if(user.is_authenticated):
        user_data = User_data.objects.get(username=user.username)
        group_data = Group_Log.objects.get(group_name=request.data['group_name'])
        # print(len(group_data.combined_shares['combined_shares']))
        if(len(group_data.combined_shares['combined_shares'])>=group_data.members_required):
            secret = reconstruct_secret(group_data.combined_shares['combined_shares'])
            # aes_decrypt(secret,group_data.image_url)
            # print(x)
            # print(group_data.)
            return Response({
                # 'secret':secret,
                'image':group_data.image.url
            })
        return Response({
                'error':'Not Enough Shares'
        })
    return(Response({'error':'User is not authenticated'},status=400))
    



# Upload Image to the Group
@api_view(['POST'])
def upload_image(request):
    user = request.user
    if(user.is_authenticated):
        # user_data = User_data.objects.get(username=user.username)
        group_data = Group_Log.objects.get(group_name=request.data['group_name'])
        print(group_data.image)
        group_data.image = request.data['image']
        group_data.save()
        return Response({
            "img_url":group_data.image.url if group_data.image else None
        })
    return(Response({'error':'User is not authenticated'},status=400))



@api_view(['POST'])
def get_group_log(request):
    user = request.user
    if(user.is_authenticated):
        group_data = Group_Log.objects.get(group_name=request.data['group_name'])
        return Response({
            "combined_shares":len(group_data.combined_shares["combined_shares"]),
            "members_required":group_data.members_required
        })



    
    return(Response({'error':'User is not authenticated'},status=400))
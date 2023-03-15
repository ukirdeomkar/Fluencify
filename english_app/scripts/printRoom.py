import random
from users_app.models import UserAdditionalModel
from fuzzywuzzy.fuzz import partial_token_set_ratio
from main_app.models import Room
from django.contrib.auth.models import User
import os 

with open('output.txt', 'w') as f:


    for i in Room.objects.all():

        print(f"User 1 : {i.user1}", file=f) 
        print(f"User 2 : {i.user2}", file=f)
        print(f"User 1 Interest : {UserAdditionalModel.objects.get(userid=i.user1).interest}", file=f)
        print(f"User 2 Interest : {UserAdditionalModel.objects.get(userid=i.user2).interest}", file=f)
        print(f"Common Interest : {i.common_interest}", file=f)
        for interest in i.common_interest.split(','):
            user1_interest = UserAdditionalModel.objects.get(userid=i.user1).interest.split(',')
            user2_interest = UserAdditionalModel.objects.get(userid=i.user2).interest.split(',')
            if interest not in user1_interest or interest not in user2_interest:
                print(f"Uncommon Interest : {interest} ------------------------------------"  , file=f)
        print("\n\n", file=f)



f.close()  
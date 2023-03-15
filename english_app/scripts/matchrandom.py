
import random
from users_app.models import UserAdditionalModel
from fuzzywuzzy.fuzz import partial_token_set_ratio
from main_app.models import Room
from django.contrib.auth.models import User



def findparthner(u):

    #wait to avoid inconsistency
    # time.sleep(5)

    current_user = u.userid
    # room = Room.objects.filter(Q(user1=current_user) | Q(user2=current_user)).last()
    # print(room)
    # if room is not None:
    #     return roomdetails(request,room)

    user1 = UserAdditionalModel.objects.get(userid=current_user.id)
    user1_fluency = user1.fluency
    user1_interest_list = user1.interest.split(',')
    print(user1_interest_list)

    # exclude_users = list(Room.objects.values_list('user1', flat=True)) + list(Room.objects.values_list('user1', flat=True))
    # user_list = UserAdditionalModel.objects.exclude(userid__in=exclude_users).exclude(id=current_user.id)
    user_list = UserAdditionalModel.objects.exclude(id=current_user.id)

    print(len(user_list))

    user2 = None 
    max_matched_percentage = 0
    max_matched_interest = []

    for user in user_list:
        print(f"Matching with {user1.userid}")
        if user.userid.id == user1.userid.id:
            continue
        user2_interest_list = user.interest.split(',')
        matched_interest_count = 0
        matched_interest = []
        for interest1 in user1_interest_list:
            for interest2 in user2_interest_list:
                if partial_token_set_ratio(interest1,interest2) > 90:
                    print(interest1,interest2)
                    matched_interest.append(interest1)
                    matched_interest_count += 1
                    break
        user1_matched_percentage = (matched_interest_count/len(user1_interest_list))*100
        user2_matched_percentage = (matched_interest_count/len(user2_interest_list))*100
        print(f"Matching with {user.userid.username} User 1 Matched {user1_matched_percentage}, \
              User 2 Matched {user2_matched_percentage}")
        if user1_matched_percentage >= 50 and user2_matched_percentage >= 50:
            max_matched_percentage = user1_matched_percentage
            user2 = user
            max_matched_interest = matched_interest
            if max_matched_percentage > 50:
                break 
            
    # import pdb;pdb.set_trace()
    if user2 == None:
        # return HttpResponse('No Match Found! Please Try Again After Sometime')
        print(f"User not matched for No One : {user1}")
        return 


    
    common_interest = ','.join(max_matched_interest)
    ruser1 = User.objects.get(id=user1.userid.id)
    ruser2 = User.objects.get(id=user2.userid.id)

    room_id = random.randint(1000,9999)
    room = Room.objects.create(user1=ruser1 , user2=ruser2 , room_id=room_id , 
                            common_interest=common_interest,matching_percentage=max_matched_percentage)

    # return roomdetails(request,room)

# for u in UserAdditionalModel.objects.all():
    # findparthner(u)

findparthner(UserAdditionalModel.objects.get(userid=User.objects.get(username='user1031').id))

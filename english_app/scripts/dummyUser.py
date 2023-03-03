import random
from django.contrib.auth.models import User
from users_app.models import UserAdditionalModel

interests = ['Reading', 'Writing', 'Cooking', 'Sports', 'Music', 'Movies', 'Traveling', 'Photography', 'Art', 'Dancing', 'Gaming', 'Hiking', 'Shopping', 'Swimming', 'Yoga', 'Food', 'Technology', 'Politics', 'Business', 'Fashion', 'Fitness', 'Pets', 'Science', 'History', 'Education', 'Nature', 'Spirituality', 'Cars', 'Motorcycles', 'Biking', 'Fishing']

for i in range(500):
    # Generate random user details
    username = f'user{i}'
    password = 'password'
    name = f'User {i}'
    age = random.randint(18, 65)
    fluency = random.choice(['1', '2', '3'])
    user = User.objects.create_user(username=username, password=password)
    user.first_name = name.split()[0]
    user.last_name = name.split()[1]
    user.save()
    num_interests = random.randint(2, 5)
    get_random_interests = ','.join(random.sample(interests, num_interests))
    user_additional = UserAdditionalModel.objects.create(
        userid=user,
        age=age,
        fluency=fluency,
        interest=get_random_interests,
    )

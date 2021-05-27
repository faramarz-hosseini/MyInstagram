# DjangoGram!
A Django powered website which allows users to sign up, sign in, follow and unfollow other
users, and publish picture-based posts which are visible in the user's profile page. Users can also see
posts that were published by people they follow in the website's activity feed. Users can also search for other users in a responsive design manner using JQuery and AJAX. Moreover, each user created has a profile which can be visited by other users. The profile can be editted (profile picture, bio, and it's visibility status) by the owner. If a profile is set to private, only the followers can see it.
Posts visible in the activity feed or any profile can be liked by by users using AJAX calls and JQuery to manipulate the DOM. 
<br></br>
## Installation
Clone the repo:
```bash
git clone https://github.com/faramarz-hosseini/MyInstagram.git
cd MyInstagram
```
Make a virtual environment:
```bash
virtualenv -p python3 .venv
```
Activate it:
```bash
source .venv/bin/activate
```
Install requirements:
```python
pip install -r requirements.txt
```
Run migrations:
```bash
python manage.py migrate
```
Run server:
```bash
python manage.py runserver
```
## Endpoints
<ul>
<li><strong>register/:</strong> Sign up page. Users can create accounts for themselves here.
<li><strong>login/:</strong> Users are redirected to this address at arrival. (No one can use the website without having logged in.)</li>
<li><strong>/:</strong> Activity feed, the home page of the website where useres can see and like posts published by people they follow</li>
<li><strong>profile/<str:username>:</strong> A specific user's profile. Users can see their and other people's profiles here. They can also edit their profile and follow, unfollow others. Posts published by the owner of the profile are also visible here and can be interacted with via liking/disliking.</li>
<li><strong>new/:</strong> While accessing this endpoint, users can publish new posts. They do this by submitting a photo and description (caption) for their post.</li>
<li><strong>notifications/:</strong> Users who have requested to follow others with private profiles, will have their requests shown here <strong>for the user they have request to follow.</strong></li> 
<li><strong>search/:</strong> Users can search for other users via a textbox here. The input from the textbox is fetched using JS, and results are shown on the page using JQuery and AJAX.
<li><strong>... And a lot more!</strong></li>
</ul>
<br>

## Technology Stack
<ul>
<li>Django (Python)</li>
<li>JavaScript</li>
<li>AJAX</li>
<li>JQuery</li>
</ul>

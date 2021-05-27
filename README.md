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
<br></br>
## Endpoints


## Technology Stack
<ul>
<li>Django (Python)</li>
<li>JavaScript</li>
<li>AJAX</li>
<li>JQuery</li>
</ul>

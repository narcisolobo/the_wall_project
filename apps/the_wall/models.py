from django.db import models

import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first-name']) == 0:
            errors['first_name_blank'] = 'The first name field cannot be blank.'
        if len(postData['first-name']) < 2:
            errors['first_name_short'] = 'The first name field must be at least 2 characters.'
        if postData['first-name'].isalpha() == False:
            errors['first_name_alpha'] = 'The first name field must contain only letters.'
        if len(postData['last-name']) == 0:
            errors['last_name_blank'] = 'The last name field cannot be blank.'
        if len(postData['last-name']) < 3:
            errors['last_name_short'] = 'The last name field must be at least 2 characters.'
        if postData['last-name'].isalpha() == False:
            errors['last_name_alpha'] = 'The last name field must contain only letters.'
        if len(postData['email']) == 0:
            errors['email_blank'] = 'Please enter your email.'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_invalid'] = 'Please enter a valid email address.'
        if len(postData['password']) == 0:
            errors['pword_blank'] = 'The password field cannot be blank.'
        if len(postData['password']) < 8:
            errors['pword_short'] = 'The password field must be at least eight characters.'
        if (postData['password'] != postData['password-confirm']):
            errors['pword_match_fail'] = 'Passwords do not match.'
        return errors
    def password_validator(self, postData):
        errors = {}
        user = User.objects.get(email=postData['login-email'])
        if not bcrypt.checkpw(postData['login-password'].encode(), user.pwhash.encode()):
            errors['pword_fail'] = 'You have entered an incorrect password.'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pwhash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message_body = models.TextField()
    posted_by = models.ForeignKey(User, related_name='messages')
    likes = models.IntegerField(default=0)
    users_who_like = models.ManyToManyField(User, related_name='liked_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment_body = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name='comments')
    likes = models.IntegerField(default=0)
    users_who_like = models.ManyToManyField(User, related_name='liked_comments')
    message_parent = models.ForeignKey(Message, related_name='child_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
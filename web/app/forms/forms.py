from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     HiddenField)
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app import images

class BlogForm(FlaskForm):
    entryid = HiddenField()
    message = TextAreaField('message',validators=[InputRequired(),Length(min=1, max=280)])
    image = FileField('Image Upload', [FileAllowed(images, 'File upload is support only image.')])

'''
<form id="addBlogBlog" hidden="hidden" enctype="multipart/form-data">
    {% if current_user.is_authenticated %}
    <input type="hidden" id="name" name="name" value="{{current_user.name}}">
    <input type="hidden" id="curr_email" name="email" value="{{current_user.email}}">
    <input type="hidden" id="avatar_url" name="avatar_url" value="{{current_user.avatar_url}}">
    <textarea type="text" id="message" name="message" maxlength="280" placeholder="message" required></textarea>
    <input type="hidden" id="entryid" name="id" value="">
    <input type="file" id="img" name="img">
    <input type="submit" id="submit_form" name="submit" value="Submit">
    <button id="clear_form" type="button">Clear</button>
    <button id="cancel_form" type="button">Cancel</button>
</form>'''


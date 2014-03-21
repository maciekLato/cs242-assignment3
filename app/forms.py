from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class CommentForm(Form):
    username = TextField('username', validators = [Required()])
    comment = TextField('comment', validators = [Required()])

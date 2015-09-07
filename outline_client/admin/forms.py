from client.forms import Form, wtf


class AddOutlineForm(Form):
    title = wtf.StringField()
    content = wtf.TextAreaField()
    author = wtf.IntegerField()
    hashtags = wtf.StringField(description='delimit by commas like #hello, #hi')

EditOutlineForm = AddOutlineForm

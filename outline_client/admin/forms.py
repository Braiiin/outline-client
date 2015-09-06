from client.forms import Form, wtf


class AddOutlineForm(Form):
    title = wtf.StringField()
    content = wtf.TextAreaField()
    author = wtf.IntegerField()


EditOutlineForm = AddOutlineForm

from wtforms import Form, TextField

class AddSearchForm(Form):
    title = TextField("Title")
    keywords = TextField("Add Keywords")

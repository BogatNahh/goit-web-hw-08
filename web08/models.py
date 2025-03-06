from mongoengine import Document, StringField, BooleanField, ReferenceField, ListField, connect

connect(db="myDatabase", host="mongodb+srv://17121t2118:<db_password>@cluster0.vulx1.mongodb.net/")

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, required=True)
    quote = StringField(required=True)

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)

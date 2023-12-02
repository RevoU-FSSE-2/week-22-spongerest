from flask_mongoengine import BaseQuerySet
from mongoengine import Document, StringField, EmailField


class UserQuerySet(BaseQuerySet):
    def to_json(self):
        return [{"id": str(user.id), "name": user.name, "email": user.email, "role": user.role, "status": user.status} for user in self]

class User(Document):
    name = StringField(required=True)
    role = StringField(required=True, choices=('user', 'admin'), default='user')
    status = StringField(required=True, choices=('active', 'inactive'), default='inactive')
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    meta = {'queryset_class': UserQuerySet}

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'status': self.status,
        }
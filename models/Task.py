from mongoengine import Document, StringField, DateTimeField


class Task(Document):
    userId = StringField(required=True)
    type = StringField(choices=['low', 'medium', 'high'], default='low')
    status = StringField(choices=['pending', 'completed'], default='pending')
    name = StringField(required=True)
    date = DateTimeField(required=True)
    time = StringField(required=True)

    meta = {'timestamps': True}

    def to_dict(self):
        print(f"Debug: Converting Task to dict, id={self.id}")
        return {
            'id': str(self.id),
            'userId': self.userId,
            'type': self.type,
            'status': self.status,
            'name': self.name,
            'date': self.date.isoformat(),
            'time': self.time
        }
    
    
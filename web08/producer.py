import pika
import json
from faker import Faker
from models import Contact
from mongoengine import Document, StringField, BooleanField, ReferenceField, ListField, connect

fake = Faker()

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

def create_contacts(n=10):
    for _ in range(n):
        contact = Contact(fullname=fake.name(), email=fake.email())
        contact.save()
        channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id))

if __name__ == "__main__":
    create_contacts(10)
    print("Контакти створені та відправлені у чергу.")

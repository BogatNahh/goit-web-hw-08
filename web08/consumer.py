import pika
from models import Contact
from mongoengine import Document, StringField, BooleanField, ReferenceField, ListField, connect

def send_email(contact_id):
    contact = Contact.objects(id=contact_id).first()
    if contact and not contact.sent:
        print(f"Відправляємо email: {contact.email}...")
        contact.sent = True
        contact.save()

def callback(ch, method, properties, body):
    send_email(body.decode())

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)
print("Очікування повідомлень...")
channel.start_consuming()

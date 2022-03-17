from django.db import models


class Chatbot(models.Model):
    '''
    NOTE: may not be needed -> simply attach view to NLTK backend

    Exposes message and reply fields for exchanging messages
    Basically, send a POST request with query MESSAGE
    The bot sends back REPLY in JSON. e.g,

    POST /api/v1/chatbot {"message": "Hi"}
    REPLY {"reply": "Hey!"}
    '''
    message = models.TextField()
    reply = models.TextField()

import redis
import json
from time import sleep
from random import randint
import os

if __name__ == '__main__':
    redis_host = os.getenv('REDIS_HOST', 'queue')
    redis_port = os.getenv('REDIS_PORT', 6379)   
    r = redis.Redis(host=redis_host, port=redis_port, db=0)
    print(f"Aguardando  mensagens...")
    while True:
        content = json.loads(r.blpop('sender')[1])
        # Simular envio de e-mails
        print(f"Enviando mensagem com assunto: {content.get('subject')}")
        sleep(randint(5, 10))
        print(f"Mensagem com assunto: {content.get('subject')} enviada!")

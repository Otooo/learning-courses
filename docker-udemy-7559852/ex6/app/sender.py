import psycopg2
import logging
from bottle import (
    Bottle,
    request
)
import redis
import json
import os

class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='GET', callback=self.test)
        self.route('/', method='POST', callback=self.send)
        db_name = os.getenv('DB_NAME', 'table')
        db_host = os.getenv('DB_HOST', 'server')
        db_port = os.getenv('DB_PORT', 5432)
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', '')
        redis_host = os.getenv('REDIS_HOST', 'queue')
        redis_port = os.getenv('REDIS_PORT', 6379)
        
        self.queue = redis.Redis(host=redis_host, port=redis_port, db=0)
        self._DSN = f'dbname={db_name} user={db_user} host={db_host} port={db_port} password={db_password}'

    def _register_message(self, subject, message):
        SQL = 'INSERT INTO emails (subject, message) VALUES (%s, %s)'
        with psycopg2.connect(self._DSN) as conn:
            with conn.cursor() as cur:
                cur.execute(SQL, (subject, message))
                conn.commit()
        msg = {'subject': subject, 'message': message}
        self.queue.rpush('sender', json.dumps(msg))

    def test(self):
        return "Funcionando"

    def send(self):
        subject = request.forms.get('subject')
        message = request.forms.get('message')

        try:
            self._register_message(subject, message)
            return f"Mensagem enfileirada! Assunto: {subject} | Mensagem: {message}"
        except Eception as e:
            return f"Error! {str(e)} - Assunto: {subject} | Mensagem: {message}"

if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)

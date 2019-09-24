from bottle import route, run, request
import logging 

@route('/', method='GET')
def test():
    return "Funcionando"

@route('/', method='POST')
def send():
    subject = request.forms.get('subject')
    message = request.forms.get('message')

    return f"Mensagem enfileirada! Assunto: {subject} | Mensagem: {message}"

if __name__ == '__main__':
    run(port=8080, debug=True)

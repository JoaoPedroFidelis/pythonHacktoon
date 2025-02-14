from twilio.rest import Client

def makeSms(msg):
    account_sid = 'AC1b3d6f02d1e30a51f0adc0ce2441a52b'
    auth_token = '8ba3605bce3a379f75a7a5ff1f4ad5fc'
    client = Client(account_sid, auth_token)

    twilio_number = ''
    recipient_number = ''
    
    message = client.messages.create(
        body=msg,
        from_=twilio_number,
        to=recipient_number
    )
    print("Mensagem enviada com sucesso!!!")
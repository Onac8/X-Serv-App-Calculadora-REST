#!/usr/bin/python3

import socket

def analize (peticion):
    try:
        operandos = peticion[1].split(',')
        op1 = int(operandos[0])
        op2 = int(operandos[1])
        op = operandos[2]
        return (op1,op2,op)
    except IndexError:
        return (0,0,"error")


def compute (op1,op2,op):
    sintaxError = False
    if op == "+":
        resultado = op1 + op2
    elif op == "-":
        resultado = op1 - op2
    elif op == "*":
        resultado = op1 * op2
    elif op == "/":
        try:
            resultado = op1/op2
        except ZeroDivisionError:
            resultado = 0;
            sintaxError = True
            print("YOU TRIED TO DIVIDE BY 0, DUDE!")

    return (resultado,sintaxError)



mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mySocket.bind((socket.gethostname(), 1234))
mySocket.listen(5)

try:
    while True:
        print('Waiting for connections')
        (recvSocket, address) = mySocket.accept()
        print('HTTP request received:')
        peticion = recvSocket.recv(2048).decode('utf-8')
        print(peticion)

        peticion = peticion.split()
        peticion = peticion[1][1:].split('/',maxsplit=1)
        pet = peticion[0] #get, put

        if pet == "PUT":
            (op1,op2,op) = analize(peticion)
            print ('Answering back...')
            recvSocket.send(bytes('HTTP/1.1 200 OK\r\n\r\n' +
            '<html><body><h1>Data received. Please insert /GET to consult the result.</h1>' +
            '</body></html>\r\n', 'utf-8'))
            recvSocket.close()

        elif pet == "GET":
            print ('Answering back...')
            (resultado,sintaxError) = compute(op1,op2,op)

            if sintaxError:
                recvSocket.send(bytes('HTTP/1.1 200 OK\r\n\r\n' +
                '<html><body><h1>YOU TRIED TO DIVIDE BY 0, DUDE!</h1>' +
                '</body></html>\r\n', 'utf-8'))
                recvSocket.close()
            else:
                recvSocket.send(bytes('HTTP/1.1 200 OK\r\n\r\n<html>' +
                '<body><h1>Result: ' + str(op1) + str(op) +
                str(op2) + ' = ' + str(resultado) +
                '</h1></body></html>\r\n', 'utf-8'))
                recvSocket.close()

except KeyboardInterrupt:
    print ("Closing binded socket")
    mySocket.close()

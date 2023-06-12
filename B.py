import time
from socket import *
from Segmento import *

ip = "127.0.0.1"
porta = 1007
socket = socket(AF_INET, SOCK_DGRAM)
socket.bind((ip, porta))

seqAtual = 0
ultimoSeqCorreto = -1


def receptor():
    global seqAtual, ultimoSeqCorreto
    segmentoRecebido, endereco = socket.recvfrom(2000)
    segmento = Segmento.fromBytes(segmentoRecebido)
    checksumRecebido = checksumFromBytes(segmentoRecebido)
    if not segmento.is_Corrupt(checksumRecebido) and segmento.seq >= seqAtual:
        seqAtual = segmento.seq
        ultimoSeqCorreto = segmento.seq
        ack = Segmento('ack', seqAtual)
        socket.sendto(ack.toBytes(), endereco)
        time.sleep(0.1)

        seqAtual += 1
        print("ok")
    else:
        ack = Segmento('ack', ultimoSeqCorreto)
        socket.sendto(ack.toBytes(), endereco)

while True:
    receptor()
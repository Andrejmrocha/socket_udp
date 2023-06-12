import time
from socket import *
from Segmento import *
from Service import segmentar

ip = "127.0.0.1"
porta = 1007
endereco = ip, porta
socket = socket(AF_INET, SOCK_DGRAM)
janela_envio = 5
seq = 0
segmentos_pendentes = []

media = 0
alpha = 0.825
beta = 0.25
desvio = 0
rtt = 5


def calcularTempo(rtt):
    global desvio, media
    media = (rtt * alpha) + ((1 - alpha) * media)
    diferenca = rtt - media

    if diferenca < 0:
        diferenca *= -1

    desvio = (diferenca * beta) + ((1 - beta) * desvio)
    t = media + (4 * desvio)
    return media, desvio, t


def retransmite(segmento):
    try:
        socket.sendto(segmento.toBytes(), endereco)
    except timeout:
        retransmite(segmento)


def enviar(mensagem):
    global seq, rtt
    # lista com mensagem segmentada em tamanhos de 1400 bytes
    mensagemSegmentada = segmentar(mensagem)

    while seq < len(mensagemSegmentada):
        med, dev, t = calcularTempo(rtt)
        socket.settimeout(t)

        for i in range(seq, min(seq + janela_envio, len(mensagemSegmentada))):
            if i >= len(segmentos_pendentes):
                segmento = Segmento(mensagemSegmentada[i], seq)
                socket.sendto(segmento.toBytes(), endereco)
                segmentos_pendentes.append(segmento)
                time.sleep(0.1)
        time1 = time.perf_counter()
        try:
            ack, adress = socket.recvfrom(2000)
            checksumACK = checksumFromBytes(ack)
            ack = Segmento.fromBytes(ack)
            if not ack.is_Corrupt(checksumACK):
                if seq <= ack.seq < seq + janela_envio:
                    time2 = time.perf_counter()
                    rtt = time2 - time1

                    segmentos_pendentes.pop(ack.seq - seq)
                    seq = ack.seq + 1
                    print("ok")

            else:
                print("erro confirmação")
                segmento = segmentos_pendentes[ack.seq - seq]
                retransmite(segmento)
        except timeout:
            print("erro tempo")
            for segmento in segmentos_pendentes:
                retransmite(segmento)


if __name__ == '__main__':
    enviar(input('mensagem: '))

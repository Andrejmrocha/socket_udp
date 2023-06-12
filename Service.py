def segmentar(mensagem):
    listaSegmentada = []
    for i in range(0, len(mensagem), 1400):
        listaSegmentada.append(mensagem[i: i + 1400])
    return listaSegmentada

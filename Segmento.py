def checksumFromBytes(segmento_bytes):
    return int.from_bytes(segmento_bytes[-2:], byteorder='big')


class Segmento:
    def __init__(self, mensagem, seq):
        self.mensagem = mensagem
        self.seq = seq
        self.k = 8
        self.cks = self.calculoChecksum()

    def calculoChecksum(self):
        # Inicializa o checksum com 0
        checksum = 0

        # Percorre cada byte dos dados
        for byte in self.mensagem.encode('utf-8'):
            # Soma o valor do byte ao checksum
            checksum += byte

        checksum += self.seq

        checksum = (~checksum) & 0xFFFF
        return checksum

    def is_Corrupt(self, checksumRecebido):
        return self.cks != checksumRecebido

    def toBytes(self):
        return self.mensagem.encode('utf-8') + self.seq.to_bytes(1, byteorder='big') \
               + self.cks.to_bytes(2, byteorder='big')

    @classmethod
    def fromBytes(cls, segmento_bytes):
        mensagem = segmento_bytes[:-3].decode('utf-8')
        seq = int.from_bytes(segmento_bytes[-3:-2], byteorder='big')
        return cls(mensagem=mensagem, seq=seq)

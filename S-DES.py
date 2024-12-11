
import numpy as np

'''
Trabalho 1 de segurança computacional
implementação do S-DES
'''

class SDES:
    def __init__(self, message, key):
        self.message = message
        self.key = self.Str2List(key)
        self.k1 = None
        self.k2 = None

    def Str2List(self, str):
        return np.array([int(bit) for bit in str])
    def List2Str(self, list):
        return ''.join(str(bit) for bit in list)

    def SubKeys(self):
        def P10(key):
            p = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
            p = [x - 1 for x in p]
            return np.array([key[bit] for bit in p])
        def P8(key):
            p = [6, 3, 7, 4, 8, 5, 10, 9]
            p = [x - 1 for x in p]
            return np.array([key[bit] for bit in p])
        
        def SL(key):
            return np.concatenate((np.roll(key[:5], 2), np.roll(key[5:], 2)))
        key = SL(P10(self.key))
        self.k1 = P8(key)
        self.k2 = P8(SL(key))

    def IP(self, m, inverse=False):
        if not inverse:
            p = [2, 6, 3, 1, 4, 8, 5, 7]
            p = [x - 1 for x in p]
        else:
            p = [4, 1, 3, 5, 7, 2, 8, 6]
            p = [x - 1 for x in p]
        return np.array([m[bit] for bit in p])
    
    def Feistel(self, k):
        def EP(m):
            p = [4, 1, 2, 3, 2, 3, 4, 1]
            p = [x - 1 for x in p]
            return np.array([m[bit] for bit in p])
        
        def XOR(m, k):
            return np.array([a^b for a, b in zip(m, k)])
        
        def SBox(m):
            s1 = [[1, 0, 3, 2], 
                  [3, 2, 1, 0], 
                  [0, 2, 1, 3], 
                  [3, 1, 3, 2]]
            s2 = [[0, 1, 2, 3], 
                  [2, 0, 1, 3], 
                  [3, 0, 1, 0], 
                  [2, 1, 0, 3]]
            m1 = m[:4]
            m1_l = int(self.List2Str([m1[0], m1[3]]), 2)
            m1_c = int(self.List2Str(m1[1:3]), 2)
            s1_value = s1[m1_l][m1_c]
            m1 = self.Str2List(bin(s1_value)[2:].zfill(2))

            m2 = m[4:]
            m2_l = int(self.List2Str([m2[0], m2[3]]), 2)
            m2_c = int(self.List2Str(m2[1:3]), 2)
            s2_value = s2[m2_l][m2_c]
            m2 = self.Str2List(bin(s2_value)[2:].zfill(2))

            return np.concatenate((m1, m2))
        
        def P4(m):
            p = [2, 4, 3, 1]
            p = [x - 1 for x in p]
            return np.array([m[bit] for bit in p])
        
        m1 = self.message[:4]
        m2 = EP(self.message[4:])
        m2 = XOR(m2, k)
        m2 = SBox(m2)
        m2 = P4(m2)
        m1 = XOR(m1, m2)
        m2 = self.message[4:]
        return np.concatenate((m1, m2))
    
    def SW(self, m):
        return np.concatenate((m[4:], m[:4]))
    
    def Cipher(self):
        self.message = self.Str2List(self.message)

        self.SubKeys()

        self.message = self.IP(self.message)
        self.message = self.Feistel(self.k1)
        self.message = self.SW(self.message)
        self.message = self.Feistel(self.k2)
        self.message = self.IP(self.message, inverse=True)

        self.message = self.List2Str(self.message)

    def DCipher(self):
        self.message = self.Str2List(self.message)
        
        self.SubKeys()

        self.message = self.IP(self.message)
        self.message = self.Feistel(self.k2)
        self.message = self.SW(self.message)
        self.message = self.Feistel(self.k1)
        self.message = self.IP(self.message, inverse=True)

        self.message = self.List2Str(self.message)


if __name__ == '__main__':

    KEY = '1010000010'
    M = '11010111'

    sdes = SDES(M, KEY)
    print("Mensagem:", M)
    sdes.Cipher()
    print("Mensagem criptografada:", sdes.message)
    sdes.DCipher()
    print("Mensagem descriptografada:", sdes.message)

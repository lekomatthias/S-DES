
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
        # Entradas para permutações
        self.p10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
        self.p8 = [6, 3, 7, 4, 8, 5, 10, 9]
        self.p4 = [2, 4, 3, 1]
        self.IPi = [2, 6, 3, 1, 4, 8, 5, 7]
        self.IPf = [4, 1, 3, 5, 7, 2, 8, 6]
        self.EP = [4, 1, 2, 3, 2, 3, 4, 1]
        # Entradas para SBox 1 e 2
        self.s1 = [[1, 0, 3, 2], 
                   [3, 2, 1, 0], 
                   [0, 2, 1, 3], 
                   [3, 1, 3, 2]]
        self.s2 = [[0, 1, 2, 3], 
                   [2, 0, 1, 3], 
                   [3, 0, 1, 0], 
                   [2, 1, 0, 3]]
        self.SubKeys()

    def PN(self, key, p):
        '''Permutação de N bits'''
        p = [x - 1 for x in p]
        return np.array([key[bit] for bit in p])

    def Str2List(self, str):
        return np.array([int(bit) for bit in str])
    def List2Str(self, list):
        return ''.join(str(bit) for bit in list)

    def SubKeys(self):
        '''Geração de sub chaves'''
        def SL(key):
            return np.concatenate((np.roll(key[:5], 2), np.roll(key[5:], 2)))
        key = SL(self.PN(self.key, self.p10))
        self.k1 = self.PN(key, self.p8)
        self.k2 = self.PN(SL(key), self.p8)
    
    def Feistel(self, k):
        '''Uma rodada de Feistel'''
        def XOR(m, k):
            return np.array([a^b for a, b in zip(m, k)])
        
        def SBox(m):
            '''Aplica as duas s box de uma vez e concatena'''
            m1 = m[:4]
            m1_l = int(self.List2Str([m1[0], m1[3]]), 2)
            m1_c = int(self.List2Str(m1[1:3]), 2)
            s1_value = self.s1[m1_l][m1_c]
            m1 = self.Str2List(bin(s1_value)[2:].zfill(2))

            m2 = m[4:]
            m2_l = int(self.List2Str([m2[0], m2[3]]), 2)
            m2_c = int(self.List2Str(m2[1:3]), 2)
            s2_value = self.s2[m2_l][m2_c]
            m2 = self.Str2List(bin(s2_value)[2:].zfill(2))

            return np.concatenate((m1, m2))
        
        m1 = self.message[:4]
        m2 = self.PN(self.message[4:], self.EP)
        m2 = XOR(m2, k)
        m2 = SBox(m2)
        m2 = self.PN(m2, self.p4)
        m1 = XOR(m1, m2)
        m2 = self.message[4:]
        return np.concatenate((m1, m2))
    
    def SW(self, m):
        '''Troca de lugar do lado direito e esquerdo'''
        return np.concatenate((m[4:], m[:4]))
    
    def Cipher(self):
        '''Cifra mensagem'''
        self.message = self.Str2List(self.message)
        
        print(f'mensagem:       {self.List2Str(self.message)}')
        self.message = self.PN(self.message, self.IPi)
        print(f'PI:             {self.List2Str(self.message)}')
        self.message = self.Feistel(self.k1)
        print(f'Feistel 1:      {self.List2Str(self.message)}')
        self.message = self.SW(self.message)
        print(f'SW:             {self.List2Str(self.message)}')
        self.message = self.Feistel(self.k2)
        print(f'Feistel 2:      {self.List2Str(self.message)}')
        self.message = self.PN(self.message, self.IPf)
        print(f'PI^-1:          {self.List2Str(self.message)}')

        self.message = self.List2Str(self.message)

    def DCipher(self):
        '''Decifra mensagem'''
        self.message = self.Str2List(self.message)
        
        self.message = self.PN(self.message, self.IPi)
        self.message = self.Feistel(self.k2)
        self.message = self.SW(self.message)
        self.message = self.Feistel(self.k1)
        self.message = self.PN(self.message, self.IPf)

        self.message = self.List2Str(self.message)


if __name__ == '__main__':

    KEY = '1010000010'
    M = '11010111'

    sdes = SDES(M, KEY)
    sdes.Cipher()
    print("Mensagem criptografada:      ", sdes.message)
    sdes.DCipher()
    print("Mensagem descriptografada:   ", sdes.message)

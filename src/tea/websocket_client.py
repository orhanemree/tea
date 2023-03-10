from typing import Type
from socket import socket

class WebsocketClient:
        
    def __init__(self, socket: Type[socket], id_):
        self.__socket = socket
        self.id       = id_

    # stolen from https://stackoverflow.com/a/30829965
    def decode_msg(self, msg: bytes) -> str:
        """
        Decode websocket message from data frame bytes to string.
        """
        byteArray      = msg 
        datalength     = byteArray[1] & 127
        indexFirstMask = 2 
        
        if datalength == 126:
            indexFirstMask = 4
        elif datalength == 127:
            indexFirstMask = 10
            
        masks = [m for m in byteArray[indexFirstMask : indexFirstMask+4]]
        indexFirstDataByte = indexFirstMask + 4
        decodedChars       = []
        i = indexFirstDataByte
        j = 0
        while i < len(byteArray):
            decodedChars.append(chr(byteArray[i] ^ masks[j%4]))
            i += 1
            j += 1
        return "".join(decodedChars)
        
    
    # stolen from https://stackoverflow.com/a/30829965
    def encode_msg(self, msg: str) -> bytes:
        """
        Encode websocket message from string to data frame bytes.
        """
        bytesFormatted = []
        bytesFormatted.append(129)
        bytesRaw = msg.encode()
        bytesLength = len(bytesRaw)
        if bytesLength <= 125:
            bytesFormatted.append(bytesLength)
        elif bytesLength >= 126 and bytesLength <= 65535:
            bytesFormatted.append(126)
            bytesFormatted.append((bytesLength >> 8) & 255)
            bytesFormatted.append(bytesLength & 255)
        else:
            bytesFormatted.append(127)
            bytesFormatted.append((bytesLength >> 56) & 255)
            bytesFormatted.append((bytesLength >> 48) & 255)
            bytesFormatted.append((bytesLength >> 40) & 255)
            bytesFormatted.append((bytesLength >> 32) & 255)
            bytesFormatted.append((bytesLength >> 24) & 255)
            bytesFormatted.append((bytesLength >> 16) & 255)
            bytesFormatted.append((bytesLength >>  8) & 255)
            bytesFormatted.append(bytesLength & 255)

        bytesFormatted = bytes(bytesFormatted)
        bytesFormatted = bytesFormatted + bytesRaw
        return bytesFormatted
    
    
    def read(self, max_buffer_size: int=1024) -> bytes:
        """
        Read message from websocket client.
        """
        msg_in_bytes = self.__socket.recv(max_buffer_size)
        if msg_in_bytes:
            return self.decode_msg(msg_in_bytes)
        return ""
    
    
    def write(self, msg: str) -> None:
        """
        Write message to websocket client.
        """
        self.msg = self.encode_msg(msg)
        self.__socket.send(self.msg)

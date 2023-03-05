from .websocket_client import WebsocketClient

from typing import Type, Union

class WebsocketServer:
        
    def __init__(self):
        self.onopen    = callable
        self.onmessage = callable
        self.onclose   = callable
        # TODO: add onerror option
        self.__clients = []
        
        
    def add_client(self, client: Type[WebsocketClient]) -> None:
        self.__clients.append(client)
        
    
    def get_clients(self) -> list:
        return self.__clients


    class Event:
        
        def __init__(self, client: Type[WebsocketClient], ready_state: int, msg: Union[str, None]=None):
            self.client      = client
            self.ready_state = ready_state
            self.data        = msg
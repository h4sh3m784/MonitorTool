import json

from threading import Event
from threading import Thread
from CallOptions import calls
from uuid import uuid4

class RPCHandler:

    def __init__(self):
        self.result = {}
        self.que = []
        self.processing = []

        handleThread = Thread(target=self.start,args=[])
        handleThread.start()

    def request(self, request):
        self.add_que(request).wait()
        return json.dumps(self.request_result())

    def start(self):
        while True:
            if len(self.que) > 0:
                request = self.que[0]
                id = request['Info']['Id']
                if id not in self.processing:
                    self.processing.append(id)
                    self.request_handler(request)

    def request_result(self):
        return dict([self.result.popitem()])

    def request_handler(self,request):

        func = request['Call']['function']
        param = request['Call']['parameters']
        event = request['Info']['Event']
        id = request['Info']['Id']

        if func in calls: #Check if call request is available.
            callResult = calls[func](param)
            self.result[id] = callResult
        else:
            self.result[id] ={"result" : "call does not exist"}

        self.pop_request() #Remove request
        
        event.set()

    def add_que(self,request):
            request = json.loads(request)
            waitEvent = Event()
            info = {
                "Id" : str(uuid4()),
                "Event" : waitEvent
            }
            request['Info'] = info
            self.que.append(request)
            return waitEvent

    def pop_request(self):
        self.processing.pop(0)
        self.que.pop(0)
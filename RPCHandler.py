import json
import threading

from CallOptions import calls
from uuid import uuid4

class RPCHandler:

    def __init__(self):

        self.result = {}
        self.que = []
        self.processing = []

        #Start a new thread, to process the request in the que.
        handleThread = threading.Thread(target=self.start_rpc_handler,args=[])
        handleThread.start()

    def request(self, request):

        #Add new call request to the que, and wait() for the event (call) to set()
        queResult = self.add_que(request)
        
        #Check if an Event was created or an error occured.
        if isinstance(queResult, threading._Event):
            queResult.wait()
        else:
            return queResult

        #Return the call functions result.
        return self.request_result()

    def start_rpc_handler(self):
        while True:
            #Check if que is filled.
            if len(self.que) > 0:
                #Get first value in the que.
                request = self.que[0]
                id = request['Info']['Id']
                #Check if the request is not already being processed.
                if id not in self.processing:
                    #Start executing the call request.
                    self.processing.append(id)
                    self.request_handler(request)

    def request_result(self):
        #Get the result in json string format: Key -> Id, Value -> call result.
        #And remove the result.
        return json.dumps(dict([self.result.popitem()]))

    def request_handler(self,request):
        #Get the call information from the request body
        func = request['Call']['function']
        param = request['Call']['parameters']
        event = request['Info']['Event']
        id = request['Info']['Id']
        #Check if the call is a available call.
        if func in calls:
            try:
                #Execute calll
                callResult = calls[func](param)
                #Store result in result dict
                self.result[id] = callResult
            except:
                self.result[id] = {"err:" : "something went wrong during call execution"}
        else:
            self.result[id] ={"result" : "call does not exist"}
        #Remove request
        self.pop_request()
        #Set the waiting event
        event.set()

    def add_que(self,request):
            
            #Load request string to dictionary.

            struct = {}

            try:
                request = request.decode('utf-8')
                struct = json.loads(request)
                #Create new waiting event.
                waitEvent = threading.Event()
                #Create additional request metadata.
                info = {
                    "Id" : str(uuid4()),
                    "Event" : waitEvent
                }
                #Add metadata to request dict.
                struct['Info'] = info
                #Add request to the que.
                self.que.append(struct)
                #Return event.
                return waitEvent
            except Exception as e:
                error = {'error' : e} 
                return json.dumps(error)

    def pop_request(self):
        #Remove request from processing.
        self.processing.pop(0)
        #Remove request from que.
        self.que.pop(0)
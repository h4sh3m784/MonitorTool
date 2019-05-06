import json
import threading

from CallOptions import calls
from uuid import uuid4
import logging


class RPCHandler:

    def __init__(self):

        logging.basicConfig(level=logging.DEBUG)

        self.result = {}
        self.que = []
        self.processing = []
        self.error = None

        #Start a new thread, to process the request in the que.
        handleThread = threading.Thread(target=self.start_rpc_handler,args=[])
        handleThread.start()

    def request(self, data):

        #Add new call request to the que, and wait() for the event (call) to set()
        queResult = self.add_que(data)
        
        #Check if an Event was created or an error occured.
        if isinstance(queResult, threading.Event):
            queResult.wait()
        else:
            return self.error

        #Confirm request result with the id

        id = self.pop_request()

        if self.confirm_request_result(id):
            return self.request_result()
        return self.error

    def start_rpc_handler(self):
        while True:
            #Check if que is filled.
            if len(self.que) > 0:
                #Get first value in the que.
                request = self.que[0]
                id = request['Info']['Id']
                #Check if the request is not already being processed.
                if id not in self.processing:
                    #Remove from que.
                    del self.que[0]
                    #Add to processing
                    self.processing.append(id)
                    #Start executing the call request.
                    self.request_handler(request)

    def request_result(self):
        #Get the result in json string format: Key -> Id, Value -> call result.
        #And remove the result.
        return json.dumps(dict([self.result.popitem()]))

    def request_handler(self,request):

        #Get the call information from the request body
        event = request['Info']['Event']
        id = request['Info']['Id']

        try:
            func = request['Call']['function']
            param = request['Call']['parameters']
            #Check if the call is a available call.
            if func in calls:
                    #Execute calll
                    callResult = calls[func](param)
                    #Store result in result dict
                    self.result[id] = callResult
            else:
                set_error_message("Function does not exist")

        except Exception as e:
            set_error_message(str(e))

        #Set the waiting event
        event.set()


    def add_que(self,request):
            #Load request string to dictionary.
            try:
                logging.debug(request)
                callDict = json.loads(request)
                #Create new waiting event.
                waitEvent = threading.Event()
                #Create additional request metadata.
                info = {
                    "Id" : str(uuid4()),
                    "Event" : waitEvent
                }
                #Add metadata to request dict.
                callDict['Info'] = info
                #Add request to the que.
                self.que.append(callDict)
                #Return event.
                return waitEvent
            except Exception as e:
                set_error_message(str(e))

    def pop_request(self):
        #Remove request from processing.
        return self.processing.pop(0)
    
    def set_error_message(self, message):
        self.error = json.dumps({"error" : message})

    def confirm_request_result(self,id):
        if list(self.result.keys())[0] == id:
            return True
        return False
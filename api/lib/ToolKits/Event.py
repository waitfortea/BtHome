__all__='addEvent','callEvent'

evnet_Dict = dict()

def addEvent(eventName: str, eventFn):
    if not eventName in evnet_Dict:
        evnet_Dict[eventName] = []
    evnet_Dict[eventName].append(eventFn)

def callEvent(eventName: str, data):
    if not eventName in evnet_Dict:
        return
    for eventFn in evnet_Dict[eventName]:
        eventFn(data)


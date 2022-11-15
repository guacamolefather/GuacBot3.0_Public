def Conditional(unPuncMessage, trigger):
    return (unPuncMessage.endswith(trigger) and ((" " + trigger) in unPuncMessage)) or (unPuncMessage.startswith(trigger) and ((trigger + " ") in unPuncMessage)) or ((" " + trigger + " ") in unPuncMessage) or (trigger == unPuncMessage)

def ReadTriggers():
    triggersList = []
    with open('data\\triggers.txt', 'r', encoding='utf-8') as reader:
        for line in list(reader):
            if "***" in line:
                line = line.split('***')[1]
                holderList = []
                for i in line.split(', '):
                    holderList.append(i)
                triggersList.append(holderList)
            else:
                triggersList.append(line.split('"')[1])
    return triggersList

def ReadResponses():
    responsesList = []
    with open('data\\reactions.txt', 'r', encoding='utf-8') as reader:
        for line in list(reader):
            if "â€™" in line:
                line = line.replace("â€™", "'")
            responsesList.append(line.split('***')[1])
    return responsesList

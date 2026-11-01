class DecisionEngine:
    def __init__(self):
        pass

    def decide(self,message,mode=None):
        if mode=="web":
            return {
                "type":"web"
            }

        if mode=="image_gen":
            return {
                "type":"image_gen"
            }

        if mode=="image":
            return {
                "type":"image"
            }

        message=message.lower()
        #calculator tools
        calculator_keyword=[
            "calculate","calculator"
        ]
        for keyword in calculator_keyword:
            if keyword in message:
                return{
                    "type":"tool",
                    "name":"calculator"
                }


        if "test tool" in message:
            return {
                "type":"tool",
                "name":"test"
            }

        memory_keyword=[
            "remember","do yo know","what do you know about me","what did i tell you",
            "what did i say","my favorite","my name","my project","did i tell you"
        ]
        for keyword in memory_keyword:
            if keyword in message:
                return{
                    "type":"memory"
                }

        knowledge_keyword=[
            "document","file","pdf","txt","docx","ppt","pptx","csv","according to",
            "in my file","excel","microsoft word","text file"
        ]
        for i in knowledge_keyword:
            if i in message:
                return{
                    "type":"knowledge"
                }
        return {
            "type":"chat"
        }
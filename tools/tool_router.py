class ToolRouter:
    def __init__(self):
        self.tools={}
    
    def register(self,name,tool):
        self.tools[name]=tool

    def run(self,name,**kwargs):
        if name not in self.tools:
            return{
                "success":False,
                "error":f"Tool {name} not found"
            }
        try:
            result=self.tools[name](**kwargs)
            return{
                "success":True,
                "result":result
            }
        except Exception as e:
            return{
                "success":False,
                "error":str(e)
            }
    def list_tools(self):
        return list(self.tools.keys())
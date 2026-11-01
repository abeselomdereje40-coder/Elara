from manager import memory_manager


class memoryRecall:
    def __init__(self):
        self.memory=memory_manager()

    def recall_projects(self,name):
        project=self.memory.find_project(name)
        if not project:
            return "Project not found"

        notes=self.memory.find_notes(project["id"])
        return {
            "project":project,
            "notes":notes
        }
        
    def recall_facts(self,keyword):
        return self.memory.search_fact(keyword)

    def recall_conversation(self,session_id):
        return self.memory.get_conversation(session_id)

    def build_context(self,session_id,message):
        context={
            "conversation":self.recall_conversation(session_id),
            "facts":self.recall_facts(message),
            "project":None,
            "knowledge":[]
        }
        return context
        
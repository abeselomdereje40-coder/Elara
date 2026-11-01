from manager import memory_manager

class contextEngine:
    def __init__(self):
        self.memory=memory_manager()

    def build_context(self,name):
        project=self.memory.find_project(name)

        if not project:
            return "project not found"

        else:
            state= self.memory.get_project_state(project["name"])
            notes=self.memory.find_notes(project["id"])
            plan=self.memory.get_plan(project["id"])

            return {
                "project":project,
                "state":state,
                "plan":plan,
                "notes":notes
            }

    def get_context(self,name):
        data=self.build_context(name)
        if not data:
            return "No data found"
        
        context=[]
        context.append(" **PROJECT** ")
        project=data["project"]
        context.append(f"Name: {project['name']}")
        context.append(f"Status: {project['status']}")
        context.append("")
        state=data["state"]

        if state:
            context.append(f"Vision: {state['vision']}")
            context.append(f"Phase: {state['current_phase']}")
            context.append(f"Module: {state['current_module']}")
            context.append(f"Current_goal: {state['current_goal']}")
            context.append(f"Next_goal: {state['next_goal']}")
            context.append(f"Completion: {state['completion']}%")
            context.append("")

        context.append(" *PLAN* ")
        for step in data["plan"]:
            context.append(f"[{step['status']}]{step['step_number']}.{step['title']}")
            context.append("")

        context.append(" **Notes** ")
        for note in data["notes"][-5:]:
            context.append(f"-{note['note']}")

        return "\n".join(context)
        
    def detect_project(self,message):
        message_lower=message.lower()
        projects=self.memory.get_all_projects()
        for project in projects:
            if project["name"].lower() in message_lower:
                return project

        return None

    def generate_context(self,session_id,message):
        context = {
            "project":None,
            "facts":[],
            "knowledge":[],
            "User":message
        }
    #search projects
        project=self.detect_project(message)
        if project:
            context["project"]={
                "info":project,
                "state":self.memory.get_project_state(project["name"]),
                "plan":self.memory.get_plan(project["id"]),
                "notes":self.memory.find_notes(project["id"])
                }
        #search facts
        context["facts"]=self.memory.search_fact(message)

        #search knowledge
        knowledge=self.memory.search_knowledge(message)
        context["knowledge"]=[]
        for result in knowledge:
            context["knowledge"].append({
                "id":result["id"],
                "title":result["title"],
                "content":result["content"]
            })
        return context

    def has_memory(self,context):
        if context["project"] is not None:
            return True
        if context["facts"]:
            return True
        if context["knowledge"]:
            return True
        return False
            
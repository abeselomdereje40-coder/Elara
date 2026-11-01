from manager import memory_manager
from memory_analyzer import memoryAnalyzer

class memory_router:
    def __init__(self):
        self.memory=memory_manager()
        self.analyze=memoryAnalyzer()

    def process(self,session_id,role,message):
        self.memory.save_conversation(
            session_id,
            role,
            message
        )
        if role != "user":
            return
        result=self.analyze.analyzer(message)

        if result.get("fact"):
            self.memory.save_fact(
                result["fact"]["value"],
                result["fact"]["catagory"]
            )
        if result.get("project"):
            project=self.memory.find_project(result["project"]["name"])
            if project:
                project_id=project["id"]
            else:
                project_id=self.memory.create_project(
                    result["project"]["name"]
                )
                self.memory.project_state(
                name =result["project"]["name"],
                vision="",
                current_phase ="Planning",
                current_module ="",
                current_goal = "",
                next_goal ="",
                completion =0)
                self.memory.add_notes(project_id,result["project"].get("note",""))

from context_engine import contextEngine

class promtBuilder:

    def __init__(self):
        self.engine=contextEngine()    

    def build(self,context):
        prompt=[]
        project=None
        info=None
        state=None

        if context["project"]:
            project=context["project"]
            info=context["project"]["info"]
            state=context["project"]["state"]
            prompt.append(" ==Active project== ")
            prompt.append(f"Name: {info['name']}")

        if state:
            prompt.append(f"Vision: {state['vision']}")
            prompt.append(f"Phase: {state['current_phase']}")
            prompt.append(f"Module: {state['current_module']}")
            prompt.append(f"Goal: {state['current_goal']}")
            prompt.append(f"Next goal: {state['next_goal']}")
            prompt.append(f"Completion: {state['completion']}")
        if project:
            prompt.append("")
            prompt.append(" ==Project Plan== ")
            for step in project["plan"]:
                prompt.append(f"[{step['status']}]{step['step_number']}.{step['title']}")

            prompt.append("")
            prompt.append(" ==Project Plan== ")
            for note in project["notes"][-5:]:
                prompt.append(f"-{note['note']}")

        #fact context

        if context["facts"]:
            prompt.append("")
            prompt.append(" ==User Facts== ")
            for fact in context["facts"]:
                prompt.append(f"-{fact['fact']}")

    #knowledge context

        if context["knowledge"]:
            prompt.append("")
            prompt.append("== saved knowledge ==")
            for item in context["knowledge"]:
                prompt.append(f"Title:{item['title']}")
                prompt.append(f"Content:{item['content']}")
                prompt.append("")

        prompt.append("")
        prompt.append(" ==Requiest== ")
        prompt.append(context["User"])

        prompt.append("")
        prompt.append("Response instruction")
        prompt.append("Use the avaliable project information if it is relevent")
        prompt.append("Do not repeat completed work")
        prompt.append("Continue from the current project state")
        prompt.append("If there is no active project answer the user's request normally")

        return "\n".join(prompt)
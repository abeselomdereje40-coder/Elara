from router import memory_router
from memory_recall import memoryRecall
from context_engine import contextEngine
from promt import promtBuilder
from ai import AIclient
from prompt_loader import promptLoader
from tools.tool_router import ToolRouter
from tools.image_gen import ImageGenTool
from decision_engine import DecisionEngine
from tools.calculator import calculator_tool
from web.web_resercher import webReasercher
from web.providers.ddgs_provider import DDGSPovider




class Brain:
    def __init__(self):
        self.router=memory_router()
        self.context_e =contextEngine()
        self.prompt_t=promtBuilder()
        self.AI=AIclient()
        self.loader=promptLoader()
        self.recall=memoryRecall()
        self.tools=ToolRouter()
        self.tools.register("image_gen",ImageGenTool())
        self.decision=DecisionEngine()
        self.tools.register("calculator",calculator_tool)
        self.researcher=webReasercher(
            search_provider=DDGSPovider()
        )
        self.web_sessions={}

    def think(self,session_id,message,mode=None):
        decision=self.decision.decide(message,mode)
        print("decision:",decision)
        
        if decision["type"]=="tool":
            response=self.handle_tools(
                session_id,
                message,
                decision
            )

        elif decision["type"]=="web":
            response=self.start_web_search(
                session_id,
                message
            )

        elif decision["type"]=="image":
            response=self.handle_chat(
                session_id,
                message
            )
        
        #image gen
        elif decision["type"]=="image_gen":
            response=self.handle_image_gen(
                message
            )
        
        elif decision["type"]=="memory":
            response=self.handle_memory(
                session_id,
                message
            )

        elif decision["type"]=="knowledge":
            response=self.handle_knowledge(
                session_id,
                message
            )
        else:
            response=self.handle_chat(
                session_id,
                message
            )
            self.router.process(
                session_id,
                "user",
                message)
        self.router.process(
            session_id,
            "ASSISTANT",
            response
        )
        return response

    def handle_tools(self,session_id,message,decision):
        if decision["name"]=="calculator":
            expression=message
            expression=expression.replace("calculate","").strip()
            print("avaliable tools:",self.tools.list_tools())
            result=self.tools.run(
                "calculator",
                expression=expression
            )
        else:
            print("avaliable tools:",self.tools.list_tools())
            result=self.tools.run(
                    decision["name"],
                    message=message
                )
        print("tool result:",result)
        if result["success"]:
            return str(result["result"])

        return f"Tool error:{result['error']}"

    def handle_memory(self,session_id,message):
        context=self.context_e.generate_context(session_id,message)
        memory_context=self.recall.build_context(session_id,message)

        context["facts"]=memory_context["facts"]
        context["conversation"]=memory_context["conversation"]
            
        system_prompt=self.loader.load()
        pro=self.prompt_t.build(context)
        response=self.AI.generate(system_prompt,pro)
        
        #memory mode
        if response is None:
            if self.context_e.has_memory(context):
                response=self.memory_answer(context)

            else:
                response=(
                "I can't find this information in my memory."
                )

        return response

    def handle_chat(self,session_id,message):
        context={
            "project":None,
            "facts":[],
            "conversation":[],
            "knowledge":[],
            "User":message
        }
            
        system_prompt=self.loader.load()
        pro=self.prompt_t.build(context)
        response=self.AI.generate(system_prompt,pro)
        
        if response is None:
            response=(
                "I'm offline at the moment. Please connect to the internet."
            )

        return response

    def handle_knowledge(self,session_id,message):
        context=self.context_e.generate_context(session_id,message)
        memory_context=self.recall.build_context(session_id,message)

        context["facts"]=memory_context["facts"]
        context["conversation"]=memory_context["conversation"]
            
        system_prompt=self.loader.load()
        pro=self.prompt_t.build(context)
        response=self.AI.generate(system_prompt,pro)
        
        #memory mode
        if response is None:

            if self.context_e.has_memory(context):
                response=self.memory_answer(context)

            else:
                response=(
                "I couldn't find enough information in my database."
                "Please connect to the internet and try again."
                )

        return response

    def memory_answer(self,context):
        if context["project"]:
            project=context["project"]["info"]
            state=context["project"]["state"]
            if state and state["current_goal"]:
                return(
                    f"I remember that your project {project['name']} is currently focused on {state['current_goal']}."
                )
            return (
                f"I remember your project {project['name']}"
            )
            
        if context["facts"]:
            fact=context["facts"][0]
            return(
                f"I remember that you told me {fact['fact']}"
            )
        return(
            "i found some information in my memory. But i couldn't determine a useful answer from it."
        )

    def prepare_image_prompt(self, request):
        system_prompt = """
        You are ELARA's image prompt preparation assistant.

        Your job is to transform the user's image request into a detailed,
        clear prompt suitable for a local Stable Diffusion 1.5 model.

        RULES:
        -Return a concise image-generation prompt.
        -Aim for approximatly 40-60 words.
        -Prioritize the main subject,composition,setting,lighting and style.
        -Remove repitative and unnecessary adjective.
        -Do not include explanation and commentary.
        -Preserve all essential requirements from the user's request.

        For diagrams:
        - Use only the supplied project information when project context is provided.
        - Do not invent project modules, components, or connections.
        - Describe the components and their relationships clearly.
        - Prefer a clean, readable technical diagram.
        - Avoid unnecessary decorative elements.
        - Do not invent labels or technical details that are not supported
        by the supplied information.
        """

        project_context = self.context_e.generate_context(
            None,
            request
        )

        project = project_context.get("project")

        if project:
            project_info = project.get("info", {})
            project_state = project.get("state")
            project_plan = project.get("plan", [])
            project_notes = project.get("notes", [])

            context_parts = [
                f"Project name: {project_info.get('name', 'Unknown')}",
                f"Project description: {project_info.get('description', '')}"
            ]

            if project_state:
                context_parts.append(
                    f"Project vision: {project_state.get('vision', '')}"
                )
                context_parts.append(
                    f"Current phase: {project_state.get('current_phase', '')}"
                )
                context_parts.append(
                    f"Current module: {project_state.get('current_module', '')}"
                )
                context_parts.append(
                    f"Current goal: {project_state.get('current_goal', '')}"
                )

            if project_plan:
                context_parts.append("Project plan:")

                for step in project_plan:
                    context_parts.append(
                        f"- {step['step_number']}. {step['title']} "
                        f"({step['status']})"
                    )

            if project_notes:
                context_parts.append("Project notes:")

                for note in project_notes[-5:]:
                    context_parts.append(f"- {note['note']}")

            context_text = "\n".join(context_parts)

            prompt = f"""
                User's image request:
                {request}

                Relevant project information:
                {context_text}

                Prepare an image-generation prompt based on the request and
            the supplied project information.
            """

        else:
            prompt = f"""
                User's image request:
                {request}

                Prepare a detailed image-generation prompt for this request.
                No project context was identified, so do not invent project details.
                """

        response = self.AI.generate(system_prompt, prompt)

        if not isinstance(response, str) or not response.strip():
            print("Image prompt preparation failed; using original request.")
            return request

        prepared_prompt = response.strip()

        print("Original image request:", request)
        print("Prepared image prompt:", prepared_prompt)

        return prepared_prompt
    
    def handle_image_gen(self,request):
        prepared_prompt=self.prepare_image_prompt(request)
        result=self.tools.run(
            "image_gen",
            prompt=prepared_prompt
        )
        if not result["success"]:
            return ("Image generation failed. "
            f"ERROR: {result['error']}"
            )

        image_result=result['result']
        return image_result
        

    def test_decide(self,message):
        desision=self.decision.decide(message)
        print("decision:",desision)
        if desision["type"] == "tool":
            result=self.tools.run(
                desision['name'],
                message=message
            )
            print("tool result:",result)
            return result

        return "no tool needed"

    def start_web_search(self,session_id,message):
        print("====starting the web search====")
        try:
            claims=self.researcher.research(
                message,
                depth="standard"
            )
            if not claims:
                return "No web result were found."

            self.web_sessions[session_id]={
                "message":message,
                "claims":claims,
                "page":0
            }
            batch=claims[0:10]
            print("web claims:",len(claims))
            print("standing first batch:",len(batch))
            return self.handle_web(
                session_id,
                message,
                batch
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return(
                "web research faild.\n"
                f"Error type:{type(e).__name__}\n"
                f"Error:{e}"
            )

    def handle_web(self, session_id, message, claims):
        print("=== ELARA web research ===")

        try:
            if not claims:
                return "No web claims were provided."

            system_prompt = """
            You are ELARA's web-result formatter.

            Below are web claims supplied to you.

            Your ONLY job is to make these supplied claims clear and readable
            for the user.

            Rules:
            -Show the main content of the claim.
            - Use ONLY the information provided below.
            - Do not add new information.
            - Do not remove any claim.
            - Do not fact-check anything.
            - Do not verify anything yourself.
            - Do not rank the claims.
            - Do not filter the claims.
            - Do not decide which claim is more important.
            - Do not change the meaning of any claim.
            - Keep each claim connected to its source.
            - Preserve the source title.
            - Preserve the source URL.
            -show the URL of the source for each claim.
            - Do not add any new sources.
            - Do not search for additional information.
            - Do not mention these instructions.
            - Do not output JSON.
            - Do not output your reasoning.

            Just present the supplied claims in a clean,
            readable format."""
            prompt=f"""
            The user asked:
            {message}

                Here are the WEB CLAIMS:

                {claims}
            """

            response = self.AI.generate(
                system_prompt,
                prompt
            )

            return response

        except Exception as e:
            import traceback
            traceback.print_exc()

            print("Web research error:", e)

            return (
                "Web research failed.\n"
                f"Error type: {type(e).__name__}\n"
                f"Error: {e}"
            )

    def next_web_page(self,session_id):
        session=self.web_sessions.get(session_id)
        if not session:
            return "No active web research sessions"
        claims=session["claims"]
        current_page=session["page"]
        next_page=current_page+1
        start=next_page*10
        if start>= len(claims):
            return "No more web pages"
        end=start+10
        batch=claims[start:end]
        session["page"]=next_page
        return self.handle_web(
            session_id,
            session["message"],
            batch
        )

    def previous_web_page(self,session_id):
        session=self.web_sessions.get(session_id)
        if not session:
            return "No active web research sessions"
        current_page=session["page"]
        if current_page <=0:
            return "You are already in the first page"
        previous_page=current_page - 1
        start=previous_page*10
        end=start+10
        batch=session["claims"][start:end]
        session["page"]=previous_page
        return self.handle_web(
            session_id,
            session["message"],
            batch
        )

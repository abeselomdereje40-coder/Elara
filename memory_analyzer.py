import json
import re
from ai import AIclient


class memoryAnalyzer:

    def __init__(self):
        self.AI = AIclient()

    def analyzer(self, message):
        message = str(message).strip()

        result = {
            "conversation": True,
            "fact": None,
            "project": None,
            "knowledge": None
        }

        if not message:
            return result

        # Ask the AI to analyze the user's message
        ai_result = self.analyze_with_ai(message)

        if ai_result is not None:
            return self.clean_result(ai_result, message)

        # If AI is unavailable, use the offline fallback
        return self.offline_analyzer(message)

    def analyze_with_ai(self, message):

        system_prompt = """
You are ELARA's memory analyzer.

Your job is to decide whether a USER message contains information
that should be remembered for future conversations.

Only extract information ABOUT THE USER.

Do NOT store:
- questions
- greetings
- normal conversation
- requests
- instructions
- opinions about other people
- information that is only temporary
- information that ELARA said
- information that the user is merely asking about

Good facts include:
- preferences
- personal interests
- skills
- long-term goals
- important personal information
- things the user explicitly says about themselves

Return ONLY valid JSON.

The JSON must have exactly this structure:

{
    "fact": {
        "category": "preference",
        "value": "The user's favorite programming language is Python."
    },
    "project": null,
    "knowledge": null
}

If there is no useful user fact, use:

{
    "fact": null,
    "project": null,
    "knowledge": null
}

For a project, only create a project when the user clearly says
they are working on, building, creating, or maintaining a project.

Never treat a question about a project as proof that the user owns
or works on that project.

For facts, rewrite the user's statement into a clear third-person
memory beginning with "The user..." or "The user's...".

Do not copy the entire user message when a shorter fact is possible.
"""

        prompt = f"""
Analyze this USER message:

{message}
"""

        try:
            response = self.AI.generate(
                system_prompt,
                prompt
            )

            if response is None:
                return None

            return self.parse_json(response)

        except Exception as e:
            print("Memory AI analyzer error:", e)
            return None

    def parse_json(self, response):

        response = str(response).strip()

        if response.startswith("```json"):
            response = response[7:]

        elif response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        try:
            return json.loads(response)

        except json.JSONDecodeError:

            start = response.find("{")
            end = response.rfind("}")

            if start != -1 and end != -1:
                try:
                    return json.loads(
                        response[start:end + 1]
                    )
                except json.JSONDecodeError:
                    pass

        print("Analyzer returned invalid JSON:")
        print(response)

        return None

    def clean_result(self, data, message):

        result = {
            "conversation": True,
            "fact": None,
            "project": None,
            "knowledge": None
        }

        if not isinstance(data, dict):
            return result

        # FACT
        fact = data.get("fact")

        if isinstance(fact, dict):
            value = fact.get("value")
            category = fact.get("category")

            if value and category:
                result["fact"] = {
                    "catagory": str(category),
                    "value": str(value)
                }

# PROJECT
        project = data.get("project")

        if isinstance(project, dict):
            name = project.get("name")

            if name:
                result["project"] = {
                    "name": str(name),
                    "description": str(
                        project.get("description", message)
                    ),
                    "note": str(
                        project.get("note", message)
                    )
                }

        # KNOWLEDGE
        knowledge = data.get("knowledge")

        if isinstance(knowledge, dict):
            if knowledge.get("title") and knowledge.get("content"):
                result["knowledge"] = knowledge

        return result

    def offline_analyzer(self, message):

        result = {
            "conversation": True,
            "fact": None,
            "project": None,
            "knowledge": None
        }

        text = message.lower().strip()

        # Questions should NEVER become facts
        if (
            "?" in message
            or text.startswith((
                "what ",
                "who ",
                "where ",
                "when ",
                "why ",
                "how ",
                "do you ",
                "did you ",
                "can you ",
                "could you ",
                "is ",
                "are "
            ))
        ):
            return result

        # Basic offline preference detection
        preference_patterns = [
            ("i like ", "preference"),
            ("i love ", "preference"),
            ("my favorite ", "preference"),
            ("my favourite ", "preference"),
            ("i prefer ", "preference"),
            ("i'm into ", "preference"),
            ("im into ", "preference")
        ]

        for pattern, category in preference_patterns:

            if pattern in text:

                result["fact"] = {
                    "catagory": category,
                    "value": message
                }

                return result

        return result

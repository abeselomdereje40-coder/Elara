from openai import OpenAI,APIConnectionError
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


class AIclient:
    def __init__(self):
        self.client=OpenAI(api_key="local",
        base_url="http://127.0.0.1:8080/v1")
    def generate(self,system_prompt,prompt):
        print("inside generate")
        try:
            response=self.client.chat.completions.create(
                model="local-model",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            print("ai call complete")
            print("response:",response)
            return response.choices[0].message.content
            
        except Exception as e:
            print("AI error:",e)
            return e
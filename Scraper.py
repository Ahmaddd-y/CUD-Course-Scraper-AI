from browser_use import Agent, Controller, SystemPrompt
from Support import Offerings

class AiAgent:
    # Initialize the AI agent with LLM, user credentials, and semester
    def __init__(self, llm, username, password, semester):
        self.llm = llm
        self.username = username
        self.password = password
        self.semester = semester
        self.controller = Controller(output_model=Offerings)

    # Main method to execute the scraping process
    async def run(self) -> Offerings:
        # Define initial browser actions to open the login page
        initial_actions = [
            {'open_tab': {'url': "https://cudportal.cud.ac.ae/student/login.asp"}}
        ]
        class MySystemPrompt(SystemPrompt):
            def important_rules(self) -> str:
                existing_rules = super().important_rules()
                # Add your custom rules
                new_rules = """
                9. MOST IMPORTANT RULE:
                
                YOU ARE NOT CREATIVE. YOU ONLY FOLLOW TASKS AS INSTRUCTED. YOU CAN NOT DO AS YOU DESIRE. 
                YOU SCRAPE DATA OUT OF THE TABLES. YOU ARE REQUIRED TO RETURN THEM IN THE END. YOU CANNOT REVIST PAGES. 
                YOU CANNOT GO BACK IN PAGES. 
                """
                return f'{existing_rules}\n{new_rules}'


        # Define the task instructions for Gemini-based or local LLM
        task = f""" 
        1. Log in to CUD Portal using username "{self.username}" and password "{self.password}" for semester "{self.semester}".
            2. Navigate to the "Course Offering" section.
            3. Click "Show Filter", select "SEAST", then click "Apply Filter".
            4. Wait for the page to fully load.
            5. Extract from the page the course data in this format:
                - **only these, ignore everything else on screen**
            {{
                "Courses": [
                    {{
                        "course_code": "...",
                        "course_name": "...",
                        "credits": "...",
                        "instructor": "...",
                        "room": "...",
                        "days": "...",
                        "start_time": "...",
                        "end_time": "...",
                        "max_enrollment": "...",
                        "total_enrollment": "..."
                    }}
                ]
            }}
            6.  Repeat this for pages 2 and 3, then stop.
                - YOU MUST KEEP TRACK OF ALL THE CONTENT YOU EXTRACTED
                - YOU MUST NOT GET LOST AND RETURN NOTHING
            7. when you are done. STOP
            8. in the end return a list that MATCHES the schema of Offerings.
            **important: YOU ARE NOT CREATIVE. YOU ONLY FOLLOW TASKS AS INSTRUCTED. YOU CAN NOT DO AS YOU DESIRE. 
                **YOU SCRAPE DATA OUT OF THE TABLES. YOU ARE REQUIRED TO RETURN THEM IN THE END. YOU CANNOT REVIST PAGES. 
                **YOU CANNOT GO BACK IN PAGES. 
                **YOU MUST DO AS YOU ARE TOLD. YOU MUST NOT RETURN "No course data found or extracted" I AM EXPECTING AN OUTCOME. 
                **YOU SHAL NOT AND CANNOT IGNORE YOUR TASK.
                **YOU ARE CAPABLE OF HANDLING LARGE AMOUNTS OF COURSES. DO NOT GET CONUFUSED OR OVERHWHELMED**
                **IN CASE YOU GET CONFUSED YOU HAVE TO ANALYZE AND USE REASONING TO CONTIUNE
            
"""


            


        # Create an agent to execute the task using the LLM and controller
        agent = Agent(
            initial_actions=initial_actions,
            task=task,
            llm=self.llm,
            controller=self.controller,
            max_actions_per_step=4,
            use_vision=False
            
        )

        # Run the agent and return the parsed result
        myResult = await agent.run()
        return self.parse(myResult)

    # Parse the result returned by the agent
    def parse(self, myResult):
        try:
            # Check if the result has a callable final_result method
            if hasattr(myResult, "final_result") and callable(getattr(myResult, "final_result")):
                final_result = myResult.final_result()
                if final_result:
                    try:
                        # Validate and return the parsed data
                        return Offerings.model_validate_json(final_result)
                    except Exception as e:
                        print(f"Failed to parse final result: {e}")
            print("Could not extract course data from result")
            return None
        except Exception as e:
            # Handle any parsing errors
            print(f"Error: {str(e)}")
            return None

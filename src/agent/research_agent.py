"""
Smart Research Agent - Main agent class that coordinates research tasks.
Uses Groq LLM for reasoning and content generation.
"""

import os 
from typing import List, Dict, Optional
from groq import Groq
from src.utils.config import Config


class ResearchAgent: 
    """AI agent that performs autonomous research tasks."""

    def __init__(self):
        """Initialize the research agent with Groq client."""
        self.config = Config()

        # Validate configuration before proceeding
        if not self.config.validate():
            raise ValueError("Invalid configuration. Please check your .env file. ")
        
        self.client = Groq(api_key = self.config.GROQ_API_KEY)
         
        # Agent state
        self.conversation_history: List[Dict] = []
        self.current_research_topic: Optional[str] = None

        print(" Research Agent initialized successfully!")
        self.config.display_config()

    def _call_groq(self, messages: List[Dict], max_tokens: Optional[int] = None) -> str:
        """
        Make a call to Groq API with error handling.

        Args : 
            messages: List of message dictionaries for this conversation
            max_tokens: Maximum tokens to generate (uses config default if None)
        Returns: 
            Generated response text
        """

        try: 
            response  = self.client.chat.completions.create(
                model = self.config.GROQ_MODEL,
                messages = messages,
                max_tokens= max_tokens or self.config.MAX_TOKENS,
                temperature= self.config.TEMPERATURE
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f" Error calling Groq API: {str(e)}")
            raise
    def test_connection(self) -> bool:
        """ Test the connection to Groq API."""
        print(" Testing Groq API connection...")

        try: 
            test_messages = [
                {
                    "role" :  "user",
                    "content": "Hello! Please respond with 'Connection succesful' to confirm the API is working. "
                }
            ]
            response = self._call_groq(test_messages, max_tokens=50)
            print(f" API Response :{response}")
            return True
        except Exception as e:
            print(f" Error testing Groq API connection: {str(e)}")
            return False
    
    def plan_research(self, topic: str) -> Dict:
        """
        Create a research plan for the given topic.

        Args: 
            topic: Research topic to Investigate

        Returns: 
            Dictionary containing research plan

        """
        print(f" Planning research for topic : '{topic}'")

        planning_prompt = f"""
        You are a research planning expert. Create a detailed research plan for the topic : "{topic}"
        
        Provide you response in this exact format:
        
        RESEARCH OBJECTIVE: [Clear, specific objective]

        KEY QUESTIONS: 
        1. [Important question to answer]
        2. [Important question to answer]
        3. [Important question to answer]

        SEARCH STRATEGY:
        - [Search approach 1]
        - [Search approach 2]
        - [Search approach 3]

        EXPECTED OUTCOMES:
        - [What we except to learn]
        - [Type of insights we'll gain]

        Keep the plan focused and actionable.

        """
        messages = [{"role":"user", "content": planning_prompt}]

        try: 
            plan_response = self._call_groq(messages, max_tokens= 500)
            self.current_research_topic = topic

            print(" research plan created")
            print(plan_response)

            return {
                "topic": topic,
                "plan":plan_response,
                "status": "planned"
            }
        except Exception as e:
            print(f" Failed to create research plan : {str(e)}")
            return {"topic" : topic, "plan": None, "status": "Failed"}
        
def main():
    """Main function to test the Research Agent"""
    print('starting smart Research Agent')

    try: 
        agent = ResearchAgent()

        # Test API connection
        if agent.test_connection():

            # test research planning
            test_topic = "artificial intelligence in healthcare"
            plan = agent.plan_research(test_topic)

            if plan["status"] == "planned":
                print("Research planning successful!")
                print("Ready to implement web search and full research workflow")
            else:
                print("\n Research planning failed")

        else:
            print("\n API connection failed. please check your API key.")

    except Exception as e:
        print(f"\n Error initializing agent: {str(e)}")
        print(" Check you .env file and API key")

if __name__ == "__main__":
    main()




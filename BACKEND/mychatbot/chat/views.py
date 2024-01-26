
import os
from django.http import JsonResponse
from django.views import View
from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.llm_symbolic_math.base import LLMSymbolicMathChain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub

class MyChatBot(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_agent = None
        self.llm_symbolic_math = None
        self.huggingface_chain = None

    def create_db_agent(self):
        OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        db = SQLDatabase.from_uri("postgresql://postgres:0987@localhost:5432/db")
        llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION
        verbose = True
        self.db_agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=verbose, agent_type=agent_type)
        self.llm_symbolic_math = LLMSymbolicMathChain.from_llm(llm)

        repo_id = 'tiiuae/falcon-7b-instruct'
        huggingface_hub_api_token = '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'
        llm_huggingface = HuggingFaceHub(huggingfacehub_api_token=huggingface_hub_api_token, repo_id=repo_id, model_kwargs={'temperature': 0.7, 'max_new_token': 500})
        template = """Questions: {questions}\nAnswer: let's give a detailed answer."""
        prompt = PromptTemplate(template=template, input_variables=["questions"])
        self.huggingface_chain = LLMChain(prompt=prompt, llm=llm_huggingface)

    def get(self, request, *args, **kwargs):
        user_message = request.GET.get('message', '')

        if not self.db_agent or not self.huggingface_chain:
            self.create_db_agent()

        response_message = self.handle_user_message(user_message)
        return JsonResponse({'message': response_message})

    def handle_user_message(self, user_message):
        math_keywords = ['solve', 'math', 'equation']
        if any(math_keyword in user_message.lower() for math_keyword in math_keywords):
            math_response = self.llm_symbolic_math.run(user_message)
            return f"Here is the result of the query:\n{math_response}"
        else:
            huggingface_response = self.huggingface_chain.run(questions=user_message)
            response = self.db_agent.run(user_message)
            user_sentence = f"You asked: {user_message}"
            response_with_user_sentence = f"{user_sentence}\nHuggingFace Response: {huggingface_response}\n{response}"

            return response_with_user_sentence
# # chat/views.py
# from django.http import JsonResponse
# import random
# import os
# from django.views import View 
# from langchain.agents import create_sql_agent
# from langchain_community.agent_toolkits import SQLDatabaseToolkit
# from langchain.sql_database import SQLDatabase
# from langchain.llms.openai import OpenAI
# from langchain.agents.agent_types import AgentType
# OPENAI_API_KEY=os.environ["OPENAI_API_KEY"]
# db=SQLDatabase.from_uri("postgresql://postgres:0987@localhost:5432/db")
# llm=OpenAI(temperature=0,openai_api_key=OPENAI_API_KEY)
# model_name='gpt-3.5-turbo'


# def get_response(request):
#     user_message = request.GET.get('message', '')
#     response_message = handle_user_message(user_message)
#     return JsonResponse({'message': response_message})

# def handle_user_message(user_message):
#     greetings = ['hi', 'hello', 'hey']
#     goodbyes = ['bye', 'see you', 'goodbye']
#     compliments = ['nice', 'awesome', 'great']

#     if user_message.lower() in greetings:
#         return 'Hello! How can I assist you today?'
#     elif user_message.lower() in goodbyes:
#         return 'Goodbye! Have a wonderful day!'
#     elif 'weather' in user_message.lower():
#         return 'The weather is currently sunny and warm.'
#     elif 'time' in user_message.lower():
#         return 'The current time is 12:34 PM.'
#     elif 'joke' in user_message.lower():
#         return get_random_joke()
#     elif 'quote' in user_message.lower():
#         return get_random_quote()
#     elif any(keyword in user_message.lower() for keyword in compliments):
#         return 'Thank you! I appreciate the compliment.'
#     else:
#         return 'I did not understand that. Please ask something else.'

# def get_random_joke():
#     jokes = ['Why did the scarecrow win an award? Because he was outstanding in his field!',
#              'What do you call fake spaghetti? An impasta!',
#              'Why did the bicycle fall over? Because it was two-tired!']
#     return random.choice(jokes)

# def get_random_quote():
#     quotes = ['The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt',
#               'The way to get started is to quit talking and begin doing. - Walt Disney',
#               'Do not wait to strike till the iron is hot, but make it hot by striking. - William Butler Yeats']
#     return random.choice(quotes)


# class MyChatBot():
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.db_agent = None  
        
#     def create_db_agent(self):
#         # Create and configure your db_agent here
#         llm = OpenAI(temperature=0)
#         toolkit =SQLDatabaseToolkit(db=db,llm=OpenAI(temperature=0))
#         agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION
#         verbose = True
#         self.db_agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=verbose, agent_type=agent_type)

#     def get(self, request, *args, **kwargs):
#         user_message = request.GET.get('message', '')

#         if not self.db_agent:
#             self.create_db_agent()  # Create db_agent if it's not already created

#         response_message = self.handle_user_message(user_message)
#         return JsonResponse({'message': response_message})

#     def handle_user_message(self, user_message):
#         # Use self.db_agent to interact with your chatbot logic
#         if self.db_agent:
#             response = "Bot's response based on user_message"
#             return response
#         else:
#             return "Chatbot not initialized. Please try again later."
# chat/views.py
# chat/views.py
# chat/views.py
# chat/views.py
# chat/views.py
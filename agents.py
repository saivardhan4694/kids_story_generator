from textwrap import dedent
from crewai import Agent
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

class StoryWritingAgents():
    def __init__(self):
        load_dotenv()

        self.llm = LLM(model = "Huggingface/https://nvm60xm0xjtpglqu.us-east-1.aws.endpoints.huggingface.cloud")
        self.llm = LLM(model="groq/llama3-70b-8192")


    def story_writing_agent(self):
        return Agent(
            role = "Children Story Writer",
            goal = "Write a story for children based on a given prompt",
            backstory = dedent("""\
                You are expert story writer for children. You have written many stories for children and have a good understanding of what they like.
                You are stories are as fun and engaging as they are educational.
            """),
            llm = self.llm
        )
    
    def story_analysis_agent(self):
        return Agent(
            role = "Story Analyst",
            goal = "Analyse the story, write detailed visual discriptions of the charecters and identify the sections of the story that could be used for generating images.",
            backstory = dedent("""\
                You are an expert story analyser. your job is to go through the story and give out detailed visual discriptions of the charecters in the story and identifing the sections of the story that could be used for generating images.
            """),
            llm = self.llm
        )
    
    def image_prompt_generator(self):
        return Agent(
            role = "Image Prompt Generator",
            goal = "Generate image prompts based on the charecter descriptions and story sections.",
            backstory = dedent("""\
                Your primary role is to use the charecter discriptions and image sections form the provided json and generate meaningful prompts for image generation models."""),
            llm = self.llm
        )
    
    def writing_assistent(self):
        return Agent(
            role = "Story Writing Assistent",
            goal = "Assist the story writer in writing the story by suggesting ideas and plot sequences based on what they have written until now",
            backstory = dedent("""\
                Your primary role is to assist the story writer in writing the story by suggesting ideas and plot sequences based on what they have written. 
                You are an expert story writer now helping children bring their imagination to life."""),
                llm = self.llm      
        )
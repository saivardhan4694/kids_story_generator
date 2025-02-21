from dotenv import load_dotenv
from crewai import Crew
from tasks import StoryGenerationTasks
from agents import StoryWritingAgents
from pydantic import BaseModel, Field

from pydantic import BaseModel, Field
from typing import List, Dict
from pathlib import Path

class StoryOutput(BaseModel):
    title: str = Field(description="The title of the story")
    story: str = Field(description="The complete text of the story")
    moral: str = Field(description="The moral or takeaway message of the story")

class CharacterDescription(BaseModel):
    name: str = Field(description="The name of the character")
    physical_description: str = Field(description="The physical traits of the character (e.g., height, appearance, clothing)")

class ImageSection(BaseModel):
    marker: str = Field(description="The marker used to indicate the section in the story (e.g., [1], [2])")
    section_text: str = Field(description="The exact section of the story text used for image generation")

class StoryAnalysisOutput(BaseModel):
    title: str = Field(description="The title of the story")
    story: str = Field(description="The story text with markers for image generation sections")
    moral: str = Field(description="The moral or takeaway message of the story")
    characters: List[CharacterDescription] = Field(description="A list of characters with their physical descriptions")
    image_sections: List[ImageSection] = Field(description="A list of sections in the story used for generating images")

class ImagePrompt(BaseModel):
    marker: str = Field(description="The marker corresponding to the section in the story (e.g., [1], [2])")
    prompt: str = Field(description="The detailed image prompt for this section")

class ImagePromptsOutput(BaseModel):
    title: str = Field(description="The title of the story")
    story: str = Field(description="The story text, including markers for image generation sections")
    moral: str = Field(description="The moral or takeaway message of the story")
    image_prompts: List[ImagePrompt] = Field(description="A list of image prompts corresponding to the numbered sections of the story")


def generate_story(user_age, story_genere, story_theme, story_prompt, story_length):
    load_dotenv()

    story_charecterstics = {
        "story_genere" : story_genere,
        "story_prompt" : story_prompt,
        "story_theme" : story_theme,
        "story_length" : story_length
    }

    tasks = StoryGenerationTasks()
    agents = StoryWritingAgents()

    # create agents
    writing_agent = agents.story_writing_agent()
    analysis_agent = agents.story_analysis_agent()
    prompt_generator_agent = agents.image_prompt_generator()

    # create tasks
    story_generation_task = tasks.generate_story_task(writing_agent, user_age, story_charecterstics, output_file=r"D:\repositories\story generation data\outputs\story.json", output_json=StoryOutput)
    story_analysis_task = tasks.analyse_story_task(analysis_agent, output_file=r"D:\repositories\story generation data\outputs\analysis.json", output_json=StoryAnalysisOutput)
    image_prompt_generation_task = tasks.generate_image_prompts_task(prompt_generator_agent, output_file=r"D:\repositories\story generation data\outputs\final.json", output_json=ImagePromptsOutput)

    story_analysis_task.context = [story_generation_task]
    image_prompt_generation_task.context = [story_analysis_task]

    crew = Crew(
        agents = [writing_agent,
                  analysis_agent,
                  prompt_generator_agent],
        tasks = [story_generation_task, 
                 story_analysis_task,
                 image_prompt_generation_task],
    )

    crew.kickoff()
    

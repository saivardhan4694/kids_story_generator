from textwrap import dedent
from crewai import Task
from pathlib import Path

class StoryGenerationTasks():
    def generate_story_task(self, agent, user_age: int, story_charecterstics: dict, 
                            output_file: str, output_json):
        return Task(
            description=dedent(f"""\ 
                Write an engaging and creative story for a user of age {user_age} based on the provided prompt. 
                The story must adhere to the guidelines outlined in the `story_charecterstics` dictionary.

                **Story Characteristics**: 
                {story_charecterstics}

                **Important Notes**: 
                1) The content of the story must be appropriate for the specified age group.
                2) The length of the story must not be below the length specified in `story_charecterstics`.
                3) Follow the story prompt exactly as described in `story_charecterstics`.
                4) Provide an appropriate title and moral for the story.
            """),
            expected_output=dedent("""\
                The expected output is a JSON object with the following keys:
                - title: The title of the story.
                - story: The story itself.
                - moral: The moral of the story.
            """),
            agent=agent,
            output_file = output_file,
            output_json = output_json
        )
    
    def analyse_story_task(self, agent, output_file: str, output_json):
        return Task(
            description=dedent("""\
                Analyze the story provided as context and extract the following details in JSON format:
                - Main characters and their physical descriptions. 
                - It is paramount that if no clear physical discriptions are povided in the story , the agent must infer them based on the context.
                - Sections of the story that can be used for generating images.
                - The number of image sections should be scaled by the length of the story. eg: 300 words story should have atleast 2 image sections. 500 words should have 3.

                **Important Notes**: 
                1) For each section selected for generating images, add a marker (e.g., [1], [2], etc.) in the story text at the corresponding location.
                2) Ensure the selected image sections are directly quoted from the story without modifying or adding new characters.
                3) Image sections should be presented in the same order as their corresponding markers in the story.
            """),
            expected_output=dedent("""\
                The expected output is a JSON object appended to the existing JSON with the following keys:
                - title: The title of the story.
                - story: The story itself, updated with section markers (e.g., [1], [2], etc.) for image generation.
                - moral: The moral of the story.
                - characters: A list of characters with their physical descriptions.
                - image_sections: A list of image sections from the story in order, each labeled with its corresponding marker (e.g., [1], [2], etc.).
            """),
            agent=agent,
            output_file = output_file,
            output_json = output_json
        )
    
    def generate_image_prompts_task(self, agent, output_file: str, output_json):
        return Task(
            description=dedent("""\
                Generate meaningful and detailed image prompts for a stable diffusion model based on the character descriptions and image sections provided in the context.
                Ensure that the prompts align with the story and are in the same order as the image sections.

                **Important Notes**:
                1) whenever a charecter is included in the prompt, its physical discriptions form the charecter discriptions in the input file must be added to the prompt.
                1) Prompts must correspond to the image sections provided in the story and follow their order (e.g., the prompt for section [1] should align with section [1], and so on).
                2) Do not shuffle the prompts or reorder the sections.
            """),
            expected_output=dedent("""\
                The expected output is a JSON object appended to the existing JSON with the following keys:
                - title: The title of the story.
                - story: The story itself, including section markers.
                - moral: The moral of the story.
                - image_prompts: A list of image prompts corresponding to the numbered sections of the story.
            """),
            agent=agent,
            output_file = output_file,
            output_json = output_json
        )
    
    def assisting_in_story_writing_task(self, agent, outputfile: str, output_json):
        return Task(
            description=dedent("""\
                Give 3 plot suggestions to the writer based on the story they have written until now which is provided as context.
                Ensure that the plot suggestions are inline with the story context and are relevent with the charecters that alredy exist in the story."""),
            excepted_output = dedent("""\
                The expected output is a Json object with the fallowing keys:
                - plot1: first plot suggestion.
                - plot2: second plot suggestion.
                - plot3: third plot suggestion."""),
            agent = agent,
            outputfile = outputfile,
            output_json = output_json 
        )

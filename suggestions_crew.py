from crewai import Crew
from tasks import StoryGenerationTasks
from agents import StoryWritingAgents
from dotenv import load_dotenv
from pydantic import BaseModel, Field

class PlotSuggestionModel(BaseModel):
    plot1: str = Field(description="first plot suggestion")
    plot2: str = Field(description="second plot suggstion")
    plot3: str = Field(description="TThird plot suggestion")

# Create the crew for assisting in story writing
def create_story_writing_assistant_crew(input_story):
    load_dotenv()

    tasks = StoryGenerationTasks()
    agents = StoryWritingAgents()

    # Create the writing assistant agent
    writing_assistant_agent = agents.writing_assistent()

    # Create the assisting in story writing task
    assisting_in_story_writing_task = tasks.assisting_in_story_writing_task(
        agent=writing_assistant_agent,
        outputfile=r"D:\repositories\story generation data\outputs\assistant_output.json",
        output_json=PlotSuggestionModel  # This could be the appropriate Pydantic model if necessary
    )

    assisting_in_story_writing_task.context = [input_story]

    # Define the crew with just the writing assistant agent and task
    crew = Crew(
        agents=[writing_assistant_agent],
        tasks=[assisting_in_story_writing_task]
    )

    return crew

# Now, you can initialize and run the crew
def suggest_plots(input_story):
    story_writing_assistant_crew = create_story_writing_assistant_crew(input_story)
    story_writing_assistant_crew.kickoff()

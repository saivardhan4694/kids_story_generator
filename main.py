import story_crew
import image_generator
import json

class StoryMain:
    def generate_story(self, user_age, story_genre, story_theme, story_length, user_prompt):

        story_crew.generate_story(
            user_age=user_age,
            story_genere=story_genre,
            story_theme=story_theme,
            story_length=story_length,
            story_prompt=user_prompt,
        )
        
        open_ai_key = "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"
        file_path = r"D:\repositories\story generation data\outputs\final.json"
        generator = image_generator.StoryImageGenerator(api_key=open_ai_key, file_path=file_path)
        generator.generate_images_and_update_prompts()
        
        
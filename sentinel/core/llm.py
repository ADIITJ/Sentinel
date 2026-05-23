import os
from typing import Optional, Any, Dict
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from pydantic import BaseModel

class LLMResponse(BaseModel):
    content: str
    usage: Dict[str, Any]
    model_name: str

class LLMRouter:
    def __init__(self, project_id: Optional[str] = None, location: str = "us-central1"):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = location
        if self.project_id:
            vertexai.init(project=self.project_id, location=self.location)
    
    def generate(self, prompt: str, task_type: str = "reasoning", model_name: Optional[str] = None) -> LLMResponse:
        """Routes prompt to appropriate model based on task type."""
        if not model_name:
            if task_type == "reasoning":
                model_name = "gemini-1.5-pro"
            else:
                model_name = "gemini-1.5-flash"
        
        model = GenerativeModel(model_name)
        
        # Adjust configuration based on task
        config = GenerationConfig(
            temperature=0.2 if task_type == "extraction" else 0.7,
            max_output_tokens=2048,
        )
        
        response = model.generate_content(prompt, generation_config=config)
        
        return LLMResponse(
            content=response.text,
            usage={"total_tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0},
            model_name=model_name
        )

# Global router instance
router = LLMRouter()

# backend/services/together_generator.py

from backend.services.llm_router import call_together_ai

def generate_using_together_ai(prompt: str, diagram_type: str) -> str:
    """
    Fallback method using Together.AI to generate PlantUML text 
    based on a prompt and diagram type. Returns PlantUML code as string.
    """
    system_prompt = f"You are a helpful assistant that generates PlantUML for {diagram_type} diagrams."
    user_input = f"Generate a PlantUML {diagram_type} diagram for: {prompt}"

    try:
        response = call_together_ai(system_prompt=system_prompt, user_input=user_input)
        return response.strip()
    except Exception as e:
        print(f"❌ TogetherAI error: {e}")
        return "@startuml\nclass Fallback {{}}\n@enduml"

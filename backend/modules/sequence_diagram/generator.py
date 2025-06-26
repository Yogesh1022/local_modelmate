def generate_sequence_plantuml(data):
    """
    Converts sequence diagram data into PlantUML code.
    """
    try:
        diagram = data.get("sequence_diagram", {})
        participants = diagram.get("participants", [])
        messages = diagram.get("messages", [])

        uml = "@startuml\n"

        # Declare participants
        for participant in participants:
            uml += f"participant {participant}\n"

        uml += "\n"

        # Add messages
        for message in messages:
            from_participant = message["from"]
            to_participant = message["to"]
            label = message["message"]
            uml += f"{from_participant} -> {to_participant} : {label}\n"

        uml += "@enduml\n"
        return uml

    except Exception as e:
        print(f"❌ Error generating sequence diagram PlantUML: {e}")
        return ""

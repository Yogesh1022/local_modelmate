def generate_usecase_plantuml(data):
    try:
        diagram = data["usecase_diagram"]
        actors = diagram.get("actors", [])
        use_cases = diagram.get("use_cases", [])
        associations = diagram.get("associations", [])

        uml = "@startuml\n"
        uml += "left to right direction\n"
        uml += "skinparam packageStyle rectangle\n\n"

        # Actors
        for actor in actors:
            name = actor.replace(" ", "_")
            uml += f'actor {name} as "{actor}"\n'

        # Use cases
        for use_case in use_cases:
            name = use_case.replace(" ", "_")
            uml += f'usecase {name} as "{use_case}"\n'

        uml += "\n"

        # Associations
        for assoc in associations:
            from_item = assoc["from"].replace(" ", "_")
            to_item = assoc["to"].replace(" ", "_")
            uml += f"{from_item} --> {to_item}\n"

        uml += "\n@enduml\n"
        return uml

    except Exception as e:
        print(f"❌ Error generating use case PlantUML: {e}")
        return ""

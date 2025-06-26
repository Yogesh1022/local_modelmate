def generate_class_plantuml(project_data: dict) -> str:
    """
    Converts a project dictionary with class diagram data into a PlantUML class diagram.
    """
    try:
        diagram = project_data.get("class_diagram", {})
        classes = diagram.get("classes", [])
        relationships = diagram.get("relationships", [])

        uml = "@startuml\n\n"

        # Generate classes with attributes and methods
        for cls in classes:
            class_name = cls.get("name", "").replace(" ", "_")
            uml += f"class {class_name} {{\n"
            for attr in cls.get("attributes", []):
                uml += f"  {attr}\n"
            for method in cls.get("methods", []):
                uml += f"  {method}()\n"
            uml += "}\n\n"

        # Generate relationships
        for rel in relationships:
            class1 = rel.get("class1", "").replace(" ", "_")
            class2 = rel.get("class2", "").replace(" ", "_")
            rel_type = rel.get("type", "association")

            if rel_type == "one-to-one":
                uml += f'{class1} "1" -- "1" {class2}\n'
            elif rel_type == "one-to-many":
                uml += f'{class1} "1" o-- "*" {class2}\n'
            elif rel_type == "many-to-one":
                uml += f'{class1} "*" o-- "1" {class2}\n'
            elif rel_type == "many-to-many":
                uml += f'{class1} "*" -- "*" {class2}\n'
            else:
                uml += f"{class1} --> {class2}\n"

        uml += "\n@enduml\n"
        return uml

    except Exception as e:
        print(f"❌ Error generating PlantUML: {e}")
        return "@startuml\nclass Error {}\n@enduml"

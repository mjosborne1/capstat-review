import xml.etree.ElementTree as ET
import csv
import json
import os

def extract_actor_name(filename):
  """Extracts the part name before '.xml' from a filename, which is the actor for the capstat."""
  if filename.endswith(".xml"):
    base_name = filename[:-4]  # Remove ".xml" extension
    parts = base_name.split('-')
    return parts[-1]  # Return the last part
  else:
    return None #Return None if the file does not end with .xml

def getDefaultValue(actor, resource, element):
    """ Given an actor and a resouce, return the default value for the element"""

def process(xmlfile,output_dir):
    """
    Process the capability statement file and write the summary to the csv file
    """
    actor = extract_actor_name(xmlfile)
    if actor is None:
        return
    data_rows = []
    # Load the XML file
    tree = ET.parse(xmlfile)
    namespace = {"fhir": "http://hl7.org/fhir"}  # Define the namespace
    resources = tree.findall(".//fhir:resource", namespaces=namespace)

    if not resources:
        print("No resource elements found in the XML.")
        return
    
    # Load actor default configuration from JSON file
    config_file = "./config/actor.json"
    try:
        with open(config_file, "r") as f:
            actor_config = json.load(f)
    except FileNotFoundError:
        print(f"Configuration file not found: {config_file}. Using empty defaults.")
        actor_config = {}

    headers = [
        "resource",
        "resourceConformance",
        "defaultResourceConformance",
        "profileConformance",
        "defaultProfileConformance",
        "interaction",
        "defaultInteraction",
        "searchParams",
        "defaultSearchParams",
    ] 

    data_rows = []

    for resource in resources:
        row_data = {
            "resource": "",
            "resourceConformance": "",
            "defaultResourceConformance": "",
            "profileConformance": "",
            "defaultProfileConformance": "",
            "interaction": "",
            "defaultInteraction": "",
            "searchParams": "",
            "defaultSearchParams": "",
        }

        # type (resource)
        type_element = resource.find(".//fhir:type", namespaces=namespace)
        row_data["resource"] = type_element.get("value") if type_element is not None else ""

        # (resourceConformance)
        confType = "resourceConformance"
        extension_elements = resource.find(".//fhir:extension/fhir:valueCode", namespaces=namespace)
        row_data[confType] = extension_elements.get("value") if extension_elements is not None else ""

        # (defaultResourceConformance)
        row_data["defaultResourceConformance"] =  actor_config[confType][actor] if actor in actor_config[confType] else ""

        # (profileConformance)
        confType = "profileConformance"
        supported_profiles = resource.findall(".//fhir:supportedProfile", namespaces=namespace)
        if supported_profiles:
            profile_list = []
            for profile in supported_profiles:
                value = profile.get("value").split("/")[-1] if profile.get("value") else ""
                value_code = profile.find(".//fhir:valueCode", namespaces=namespace)
                conformance = value_code.get("value") if value_code is not None else ""
                profile_list.append(f"{value}:{conformance}")
            row_data[confType] = ",".join(profile_list)
        
        # (defaultProfileConformance)
        row_data["defaultProfileConformance"] =  actor_config[confType][actor] if actor in actor_config[confType] else ""

        # interaction
        interaction_elements = resource.findall(".//fhir:interaction", namespaces=namespace)
        if interaction_elements:
            interaction_dict = {}
            for interaction in interaction_elements:
                value_code = interaction.find(".//fhir:valueCode", namespaces=namespace)
                code = interaction.find(".//fhir:code", namespaces=namespace)
                if value_code is not None and code is not None:
                    code_value = code.get("value")
                    interaction_dict[code_value] = f"{value_code.get('value')} {code_value}"

            ordered_interactions = []
            for interaction_type in ["read", "search-type", "create", "update"]:
                if interaction_type in interaction_dict:
                    ordered_interactions.append(interaction_dict[interaction_type])

            row_data["interaction"] = ", ".join(ordered_interactions)

        # defaultInteraction
        if "interaction" in actor_config and actor in actor_config["interaction"]:
            default_interactions = actor_config["interaction"][actor]
            if default_interactions:
                default_interaction_list = []
                for code, value in default_interactions.items():
                    default_interaction_list.append(f"{value} {code}")
                row_data["defaultInteraction"] = ", ".join(default_interaction_list)
        else:
            row_data["defaultInteraction"] = ""

        # searchParam
        confType = "searchParams"
        search_param_elements = resource.findall(".//fhir:searchParam", namespaces=namespace)
        if search_param_elements:
            search_params_list = []
            for search_param in search_param_elements:
                name = search_param.find(".//fhir:name", namespaces=namespace)
                value_code = search_param.find(".//fhir:valueCode", namespaces=namespace)
                if name is not None and value_code is not None:
                    search_params_list.append(f"{name.get('value')}:{value_code.get('value')}")
            row_data[confType] = ",".join(search_params_list)
        row_data["defaultSearchParams"] =  actor_config[confType][actor] if actor in actor_config[confType] else ""
        
        # default search parameters
        if confType in actor_config and actor in actor_config[confType]:
            default_params = actor_config[confType][actor]
            if default_params:
                default_search_params_list = []
                for name, value in default_params.items():
                    default_search_params_list.append(f"{name}:{value}")
                row_data["defaultSearchParams"] = ",".join(default_search_params_list)
        else:
            row_data["defaultSearchParams"] = ""

        data_rows.append(row_data)
    xml_name = os.path.basename(xmlfile)
    output_tsv = os.path.join(output_dir, f"{actor}.tsv")
    with open(output_tsv, "w", newline="", encoding="utf-8") as tsvfile:
        writer = csv.DictWriter(tsvfile, fieldnames=headers, delimiter="\t")
        writer.writeheader()
        writer.writerows(data_rows)

    print(f"Processed {xml_name} and wrote to {output_tsv}")


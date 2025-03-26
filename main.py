import os
import shutil
import parse_capstats
import argparse

def build_path(path,recreate=False):     
    if os.path.exists(path):
        if recreate: 
            shutil.rmtree(path)
            os.makedirs(path) 
    else:    
        os.makedirs(path)

def main():
    """
    Process the capability statement files and generte a summary of Resource, Interaction, Search and Profile capabilities
    """
           
    homedir=os.environ['HOME']
    capstatdir=os.path.join(homedir,"Development","hl7au","mjo-au-fhir-erequesting","input","resources")
    datadir=os.path.join(homedir,"data","capstat-review")
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process FHIR CapabilityStatement XML files.")
    parser.add_argument(
        "--capstatdir",
        default=capstatdir,
        help=f"Directory containing CapabilityStatement XML files (default: {capstatdir})"
    )
    parser.add_argument(
        "--datadir",
        default=datadir,
        help=f"Directory to store processed capability statement summaries (default: {datadir})"
    )

    args = parser.parse_args()
    build_path(args.datadir)

    # Read the xml files from the resources directory
    for file in os.listdir(args.capstatdir):
        if file.endswith(".xml"):           
            xmlfile = os.path.join(args.capstatdir, file)
            parse_capstats.process(xmlfile,args.datadir)
    
if __name__ == "__main__":
    main()

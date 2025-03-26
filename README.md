# Capability Statement Processor  

This script processes **FHIR CapabilityStatement** XML files and generates a summary of conformance requirements for Resources, Interactions, Searches, and Profiles.  

## **Prerequisites**  

- Python 3 installed  
- `venv` module for virtual environments  
- Required Python dependencies  

## **Setup Instructions**  

### **1. Create and Activate a Virtual Environment**  

Run the following commands in your terminal:  

```sh
# Navigate to the script directory
cd /path/to/your/script

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate   # On macOS/Linux
.venv\Scripts\activate    # On Windows (Command Prompt)
.venv\Scripts\Activate.ps1 # On Windows (PowerShell)

# install requirements
pip install -r requirements.txt
```
### **2. Check that default conformance config is correct

The default conformance rules are stored in ./config/actor.json
Change the conformance words or actors as required.

### **3. Run the script

Help on arguments can be displayed using

```sh
python3 main.py -h

usage: main.py [-h] [--capstatdir CAPSTATDIR] [--datadir DATADIR]

Process FHIR CapabilityStatement XML files.

options:
  -h, --help            show this help message and exit
  --capstatdir CAPSTATDIR
                        Directory containing CapabilityStatement XML files (default: /Users/osb074/Development/hl7au/mjo-au-fhir-erequesting/input/resources)
  --datadir DATADIR     Directory to store processed capability statement summaries (default: /Users/osb074/data/capstat-review)

# example 1: using defaults on Linux/Mac
cd /path/to/your/script
python3 main.py

# example 2: setting command args on Linux/Mac
cd /path/to/your/script
python3 main.py --capstatdir /Users/osb074/git/au-fhir-erequesting/input/resources --datadir /Users/osb074/data/igreviewsc

# example 3: setting command args on Windows (untested)
cd /path/to/your/script
python3 main.py --capstatdir C:\Users\Osb074\git\au-fhir-erequesting\input\resources --datadir C:\Users\Osb074\data\igreviews

```
### **4. Check for errors

Example output with no errors:
```
Processed au-erequesting-filler.xml and wrote to /Users/osb074/data/capstat-review/filler.tsv
Processed au-erequesting-placer.xml and wrote to /Users/osb074/data/capstat-review/placer.tsv
Processed au-erequesting-server.xml and wrote to /Users/osb074/data/capstat-review/server.tsv
Processed au-erequesting-patient.xml and wrote to /Users/osb074/data/capstat-review/patient.tsv
```
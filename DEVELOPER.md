   
# Developer Readme

This Readme file extends upon the main [README](README.md). It aims to take out of sight the heavy-lifting process of extending the functionality of this integration.
    
## Adding Functionality

The process of adding functionality to this integration requires a few steps. 

1. First, we define the proper Functions/Workflows/Rules/Scripts on the Resilient UI.
2. Then we create a snapshot in the UI, and then
3. we use the `resilient-circuits codegen` command to export what we've created in __Step 1__.

### Exporting Existing Customization

1. On the resilience UI: Click "Organization Settings --> Export (to make a snapshot)"
2. Use the `resilient-circuits codegen` to create the code framework. Run this folder from one folder up of the main project folder (annoying, but the guys resilient are working on a fix)


    resilient-circuits codegen -p algosec_resilient \
        --function \
            algosec_isolate_host_from_network \
            algosec_check_host_internet_connectivity \
            algosec_list_associated_applications \
        --rule \
            "Isolate from Network (AlgoSec)" \
            "Example: AlgoSec: Check Host Internet Connectivity" \
            "Example: AlgoSec: List Associated Applications" \
        --workflow \
            example_algosec_isolate_host_from_network \
            example_algosec_check_host_internet_connectivity \
            example_algosec_list_associated_applications \
        --datatable \
            algosec_isolation_requests \
            algosec_internet_connectivity_queries \
            algosec_associated_applications
        

### Adding New Components

TL;DR: In this process we first install this customization on the server, then using the Resilient Customization UI we'll add function/workflows. Then we'll export this info and use the `codegen` tool to make the magic and create the integration python files locally:

1. Install this customization on the server:

    1. First, make sure the latest version of this customization is running on your Resilient server by running:
        `resilient-circuits customize`
        
2. Now creating the components on Resilient's UI:
    1. Creating the Function: Go to "Customization Settings --> Functions" and click on "New Function" and populate the required fields. You may use the existing "AlgoSec: Isolate Host From Network" function as an example:
        1. __Name__: use something like "AlgoSec: Isolate Host From Network" while keeping the "AlgoSec: " prefix. 
        2. __Message Destination__: Choose `algosec`. 
        3. __Description__: Add good description of the function's input/results.
        4. __Inputs__: Define the proper "Inputs" of the function or use the existing "algosec_hostname" input variable.
        5. When you are done, hit the "Save & Close" button.
    2. Creating the Workflow: Click the "Workflows" tab and hit "New Workflow".
        1. __Name__: Name it something like "Example: AlgoSec: Isolate Host From Network" by keeping the "Example: AlgoSec: " prefix. That will help prospect customers to distinguish the workflows shipped with the customization from workflows they built themselves.
        2. __API Name__: Unless you have a good reason, keep the generated value.
        3. __Description__: A good description of the Workflow.
        4. __Object Type__: Choose the object type that the workflow is relevant to.
        5. Now design the workflow in the editing window. You can use the "Example: AlgoSec: Isolate Host From Network" workflow as an example. Generally it should define the following components:
            1. Starting point.
            2. The function we defined in the previous step.
            3. Endpoint.
            4. Optional: For the function, you can specify pre/post processing scripts. These help to prepare the input for the function and process the output from the function. An example for a more advanced usage (that can be seen in "Example: AlgoSec: Isolate Host From Network") is to populate a custom data table with the function results. For now, most of our workflows use this scenario so feel free to copy the post processing logic and start from there. You may also find this [section](#debugging-workflow-pre-and-post-processing scripts) helpful.
        6. When you are done, hit the "Save & Close" button.
    3. Creating the Rule. Click the "Rules" tab:
        1. and after clicking the "New Rule" select one of:
            1. Automatic - These are triggered automatically by a set of pre-defined rules.
            2. Menu item  - These will be triggered by a user action from a "Menu Item". They also accept custom input during the menu item click.
        2. Once chosen, in the "New Rule" page, fill up the details:
            1. __Display Name__: Something like "Example: AlgoSec: Isolate Host From Network". Keep the "Example: AlgoSec: " prefix as we've done before.
            2. __Object Type__: Choose the same object type that was chosen while creating the workflow.
            3. __Conditions__: Choose the conditions from triggering this rule. An example for that can be "When an Artifact is created and Artifact type is IP Address".
            4. __Workflows__: Choose the Workflow we've created in the previous step.
            5. Hit "Save & Close".
    4. Optional: Create a __Data Table__. Only if your workflow requires a data table:
        1. Go to "Layouts" --> "Incident Tabs" --> and click one of the tabs such as "Details".
        2. On the right side menu under __Data Tables__ hit "__Add Table__".
        3. Name it while including the "AlgoSec " prefix. Something like "AlgoSec Isolation Requests" can work. 
        4. Choose and define the table columns.
3. __Export__: Now, we'll prepare all these for export and later usage by the `codegen` command. This step will create an export snapshot that will be stored by the server. Later, our tools will query and use this export snapshot. 
    1.  Go to "Administration Settings" --> "Organization" --> Hit "Export" on the left side menu.
    2. Simply click the "Export" button and ignore the file the download would be triggered for.
4. __Prepare command for codegen__: Using the `resilient-circuits codegen` command we will export all the newly created UI objects __AND all the previous ones we already defined in this integration__. If'll you export only the new components, the integration for the previous ones will break. So proceed with caution. 
    * Extend (and update in this file) the command defined in the "[Generating integration code with code gen](#exporting-existing-customization)" section:
        * For each function add it after the existing `--function` in the command. 
        * For each rule add  it after the existing `--rule` in the command. 
        * For each workflow add  it after the existing `--workflow` in the command. 
        * For each data table add  it after the existing `--datatable` in the command.
        * A good example for you to use is the already existing command line in the section mentioned.
5. __Running the `codegen` command__: In this section we'll prepare for the execution of the `codegen` command and move some files around after the command has run.
    1. __Deleting files we want to update__: The `codegen` command won't override any existing files. Therefore we have to manually delete files we want to freshen up. These files should be removed:
        1. `rm algosec_resilient/util/customize.py`
    2. __Run the `codegen` command__: After updating the command in the "[Generating integration code with code gen](#Exporting-Existing-Customization)" section, simply go one folder above the root folder of this project and execute the `codegen` command.
    3. __Moving Files Around__ - Some file has to be organized in their proper folders:
        1. Move the new files created in `algosec_resilient/tests` to `algosec_resilient/integration_tests`.
    4. __Creating unit test files__: Create the proper unit test file in the `algosec_resilient/tests` folder for the new files created in the `components` folder. The filename is usually exactly like the new file that you have just moved to the `algosec_resilient/integration_tests` folder.
6. __Publish Function Support__: List your new Function in the `setup.py` file in the `FUNCTION_COMPONENTS` dict.
7. __Updating the customization__: Anytime you update the definition of the Rules/Function/Workflows on the Resilient server, repeat steps 3 and 5.

### Debugging workflow pre and post processing scripts

The pre/post processing scripts of the Workflows in this integration can be sometimes tricky to debug before they reach their final stages. To help with that, as part of this integration we ship a script called "Example: AlgoSec: testing a workflow postprocessing". Once this integration is installed you can use it to test pre/post processing scripts.

To use it, simply:
1. Navigate to "Customization Settings" --> "Scripts" --> "Example: AlgoSec: testing a workflow postprocessing".
2. Copy the whole pre/post processing script from the workflow into the script's body.
3. Copy the output example from the docstring in the top of the file and add this line to the top of the file:
    
        results = "<example-output-from-docstring-goes-here>"
4. Hit "Run", choose an incident ID and see how that goes or if you have any errors :) The Resilient Team implemented a beautiful in-browser output shell. If your Workflow is intended to add rows to a data table it would be reflected in the output shell screen. Any exception would be visible as well. That's cool.

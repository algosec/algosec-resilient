# algosec-resilient [![Build Status](https://travis-ci.com/algosec/algosec-resilient.svg?branch=master)](https://travis-ci.com/algosec/algosec-resilient) [![Codecov](https://img.shields.io/codecov/c/github/algosec/algosec-resilient.svg)](https://codecov.io/gh/algosec/algosec-resilient)

## TOC

1. [What's In This Package](#What's-In-This-Package)
    1. Isolate IP From The Rest Of Your Network
    2. List Associated Applications
    3. Check If A Given IP Is Connected To The Internet
2. [Installation & Configuration](#installation-&-configuration)
    1. [TL; DR](#TL;-DR) - For the brave souls who wish to skip the instructions altogether.
    2. Or a [Step by Step](#Installation) for a full in-depth explanation of each step we make.
3. [Things You Should Know To Extend This Integration](#Development) (You should definitely totally ignore this section completely if you are just here to use this module =) )


## What's In This Package

The integration demonstrates key features offered by AlgoSec to simplify and enhance the security researcher's workflows. This package is also intended to support developers who wish to extend the functionality already offered. This package features 3 integration workflows:

1. Isolate IP Address From The Rest Of The Network - 
2. List Associated Application By IP - 
3. Check Internet Connectivity By IP - 

Please remember that each function is shipped both independently and as a part of a greater Workflow/Rule/Data Table example. To make it simple, please keep this in mind:

* Each __Function__ is implemented as code in this module, and is imported into the Resilient UI.
* Each __Function__ is shipped alongside an example __Workflow__. This __Workflow__ will call the __Function__ and will populate the results in a __Data Table__ that is also shipped together with this integration.
* To see the results of the example __Workflows__, don't forget to [customize the incident layout with the AlgoSec tab](#configure-incident-layout) with the relevant Data Tables. 
* Each one of the __Workflows__ are triggered by example __Rules__ shipped with this integration.
* Some of the __Rules__ are automatic upon Incidents/Artifacts creation, and some are set to trigger when a specific menu-action is clicked.

### Isolation Request

#### Configuration

As mentioned, the isolation request function will create a new Traffic Change Request on AlgoSec FireFlow. To modify the default values that are used to create this Change Request you can simply modify values in your `app.config` file. 

The fields are:
* `isolation_request_description`- The description of the new Change Requests.
* `isolation_request_template`- The name of the Template that would be used for new Change Requests.
* `isolation_request_subject`- The Change Request subject. __Note__: Keep the `{}` somewhere in the string, as it would stand for the IP that isolation request is about.
* `isolation_request_requestor_email`- The Change Request Requestor Name.
* `isolation_request_email`- The Change Request Requestor email.


### List Associated Applications

### Check Internet Connectivity

#### Configuration

As mentioned, the internet connectivity check function will use AlgoSec Firewall Analyzer. The Firewall Analyzer query will check if the given IP has access to a specific Internet Node with a specific traffic service. By default we check if there is connectivity to `http` on `8.8.8.8`. To modify the default values that are used for this traffic simulation query simply modify values in your `app.config` file. 

The fields are:
* `internet_connectivity_check_external_ip`- Defaults to `8.8.8.8`.
* `internet_connectivity_check_service`- Default to `http`.

## Installation & Configuration

### TL; DR

You are busy, you have no time for explanations. We get it, you'll catch up with all the explanations later...right?

1. Run this:
    
        python setup.py install # get the custom functions working
        resilient-circuits config -u # Create the `algosec` section in your resilient app config.
        vim ~/.resilient/app.config # Edit the connection details in the `algosec` section.
        resilient-circuits customize # Import all of the Functions/Workflows onto the Resilient UI
    
2. [Add The AlgoSec Tab To The Incident Layout](#configure-incident-layout)
3. Run the `resilient-circuits` server to handle Function calls from the Resilient Server:


        resilient-circuits run

### Installation

To quickly install the package run:

    # To install the custom function integration components
    python setup.py install

### Configuration

Once the package is installed, we'll need to add the default `algosec` settings into your default configuration file:

    # To add the `algosec` section into your existing config
    resilient-circuits config -u

Now, we'll need to update the settings with valid connection details to your AlgoSec server. The configuration file is usually found at `~/.resilient/app.config` but you should have seen the exact path in the output of the previous command. 

The `algosec` settings contain both required and optional fields. Start by modifying the required fields. Unless you have specific needs, the rest of the configuration fields can be left untouched for now.

__Required Fields__ - Make sure you update these fields before continuing:
* __server_ip__: Pointing to your AlgoSec server.
* __user__: The username that would be used to create the API connection to AlgoSec.
* __password__: The API password for the given user.
* __ssl_enabled__: Enabled by default. If you are running demo/test environment, good chance you'll need to set this one to `false`.

__Optional Fields__ - The optional fields are used by the specific custom integrations. Therefore, we'll go through them when necessary as we go into more details with the specific custom integration functions.

### Customizing The Resilient UI

Before we can get this integration running, we'll have to deploy custom settings onto your Resilient Server. This is a standard procedure that will be handled by the `resilient-circuits` package. Once your run this command, you'll see new Functions, Workflows, Rules and Data Tables, all marked by the `AlgoSec: ` or `Example: AlgoSec: ` prefixes. Then we'll continue to manually customize the Incident Tabs Layout so we can see the results of the new AlgoSec custom integration Workflows on your Resilient server.

#### Import Functions/Workflows/Rules/Data

Simply run this:

    resilient-circuits customize
        
#### Configure Incident Layout

All of the example Workflows are adding their results into dedicated Data Tables which are also shipped as part of this integration. In this step we will add a new "AlgoSec" tab to our incident layout so we can interactively see the helpful output of this integration.

To add the new AlgoSec tab to your incident layout:

1. On the Resilient UI, go to __Customization Settings__ --> __Layout__ --> __Incident Tabs__ (on the left sidebar).
2. Click __Add Tab__, input __AlgoSec__ for the __Tab Text__ and hit __Add__.
3. Now you are on the page dedicated to the __AlgoSec__ Incident.
4. On the right-hand side you'll see a box titled __Data Tables__. Simply drag and drop these Data Tables into the dashed-line box in the center column:
    1. AlgoSec Associated Applications
    2. AlgoSec Internet Connectivity Check
    3. AlgoSec Isolation Requests
5. Hit __Save__ and you are done. From now on you'll have the AlgoSec tab for all Resilient incidents. 

### Run The Integration

Now, to handle Function calls triggered by the the Resilient server, you'll need to run the `resilient-circuits` server. After you have followed the steps above all you have to do is:

    resilient-circuits run
    
__YAY!!!__ It is done! Now you should be able to use the example Workflows/Functions through the Resilient UI!

## Development

__NOTE__: This section is intended only for experienced users who wish to support or extend the functionality of this integration.

It contains in-depth explanations and how-tos for:

* Setting up development environment.
* Implementing additional custom integration Functions.
* Testing - Running integration tests, where the unit tests live etc...  

### Virtual Environment

We use `pipenv`. So it is all pretty easy. Just run `pipenv install --dev` and you've got the whole development python environment ready.

All the rest of the development commands below assume you've run `pipenv shell` beforehand to execute everything in the project's context.

### Useful Command-Line Tools


* `resilient-circuits` is the gateway for the most powerful tools built by the Resilient Team.
* `resilient-circuits list` would show the full list of custom integration components installed in this python environment.
* `resilient config -c/-u` will create or update the default Resilient Circuits configuration found at `~/.resilient/app.config`.

### Disable SSL verification

If your AlgoSec environment is a demo/test environment, you'll probably want to turn off SSL verification.

To do so, change the settings in the `algosec` section in the global `app.config` file. The file us usually found at `~/.resilient/app.config`:
 
    # Change this
    ssl_enabled=true
    
    # To This
    ssl_enabled=false   
    
### Testing

This module contain two levels of testing: 
* __Unit Tests__ - Testing code functionality without accessing live services or spinning the `resilient-circuits` app.
* __Integration Tests__ - These test the functionality of the Resilient Functions defined in the module by triggering the proper events on a demo/real resilient environment. 

#### Unit Tests

Simple by-the-book unit tests + coverage reports that are being executed by `pytest` and tested over several environments using `tox`. These tests live under `algosec_resilient/tests`

To run these tests using the current python interpreter simply run:

    pytest
    
Or to run using `tox` for all python environments (python 2.7, 3.5 and 3.6) simply run:

    tox

#### Integration Tests

Generally integration tests are implemented for two stages: 1. When testing the Resilient Circuits server and function locally, and 2. When the customization is already installed on the server and we would like to verify that the customization is installed and is working as intended. Same code base is used for these two modes with a slight modification to the configuration of running each.

These tests live under `algosec_resilient/integration_tests` and the skeleton of each file is generated by the `resilient-circuits codegen` command. The implemented functions are triggered by a specific queue message event and their output is then verified. 
1. __Test Mode__: A local resilient-circuits server is spin up using the `pytest-resilient-circuits` package. Then, the function in this code will be triggered and verified against a live local AlgoSec server.
2. __Real Server Mode__: The integration tests are running against a __LIVE__ server that has this customization installed on it. Then, the function of this module, installed on the server, will be triggered and their output will be verified.

__Note__: On both modes, the integration tests will hit a __REAL__ AlgoSec server as defined in your config.

To direct the integration tests against a an actual Resilient server add the `--real-resilient-server` option. To run the tests simply run the line below:

    pytest integration_tests --resilient_app_config=<full-path-to-your-real-app-server> (usually found in <home_folder>/.resilient/app.config) [--real-resilient-server]
    
    
### Adding Functionality

The process of adding functionality to this integration requires a few steps. 

1. First, we define the proper Functions/Workflows/Rules/Scripts on the Resilient UI.
2. Then we create a snapshot in the UI, and then
3. we use the `resilient-circuits codegen` command to export what we've created in __Step 1__.

Since this process is pretty instruction-heavy, all of the details have been moved to a separate [DEVELOPER.md](DEVELOPER.md) readme file.

## License

MIT. 

See the full license [here](LICENSE).

## Contribution

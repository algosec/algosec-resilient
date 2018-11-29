# algosec-resilient




## Generating integration code with code gen

Create the proper configuration for our functions, workflows, custom incident fields, data tables and rules. Then:

1. On the resilience UI: Click "Organization Settings --> Export (to make a snapshot)"
2. Use the `resilient-circuits codegen` to create the code framework. Run this folder from one folder up of the main project folder (annoying, but the guys resilient are working on a fix)

 
    resilient-circuits codegen -p algosec_resilient \
        --function algosec_isolate_host_from_network \
        --rule "Example: AlgoSec: Isolate Host From Network" \
        --workflow example_algosec_isolate_host_from_network \
        --datatable algosec_isolation_requests
        
## Configuring the layout for the AlgoSec incident tab

Here we will add a new tab for incidents and we will add all the fields that are relevant for our integration

1. AlgoSec Isolation Requests data table
2. AlgoSec Open To Internet
3. AlgoSec Associated Applications 

## Isolation Request

### Configure the incident layout

Once an Isolation request is successfully created, its full details including the change request url will show up in the "AlgoSec Isolation Requests" data table. To see this table, we'll have to customize the incident layout to include that table. To do so, we can follow these steps:

1. Go to "Customization Settings".
2. On the sidebar on the left, click "Incident Tabs".
3. You can add the "AlgoSec Isolation Requsets" in each of the incidents tab. For now we'll 
        
## Development

### Disable ssl verification

In the algosec configuration in the global `app.config` or `util/config.py` file, change `ssl_enabled=true` to `ssl_enabled=false`.

### Change request settings

It is possible to set and customise the different fields that are used while creating the isolation change requests. Each field can be customized by editing its field in the configuration:
* CR Description - `isolation_request_description`.
* CR Template - `isolation_request_template`.
* Subject - `isolation_request_subject`. __Note__: Keep the `{}` somewhere in the string, as it would stand for the hostname that isolation request is about.
* CR Requestor Name- `isolation_request_requestor_email` - .
* CR Requestor email - `isolation_request_email` - .


`resilient-circuits customize`
`resilient-circuits config -u`
`resilient-circuits run`

## Testing your Function Interactively ( take it from the powerpoint)

## Testing workflow pre/postprocessing scripts using the scripts section

Explain how using the example results, the post-precessing scripts can be created as regular scripts and tested for errors etc...
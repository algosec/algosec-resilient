# algosec-resilient



## Generating integration code with code gen

Create the proper configuration for our functions, workflows, custom incident fields, data tables and rules. Then:

1. On the resilience UI: Click "Organization Settings --> Export (to make a snapshot)"
2. Use the `resilient-circuits codegen` to create the code framework

 
    resilient-circuits codegen -p algosec --output-base . \
        --function algosec_isolate_host_from_network \
        --rule "Example: AlgoSec: Isolate host from network" \
        --workflow example_algosec_isolate_host_from_network \
        --datatable algosec_isolation_requests
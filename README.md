# AGVN Main

The main place to store the display-server logic. For other things like experimental stuff, admin stuff, supporting stuff, use other repos.

- should be mostly for the main server and microservices, as well as the graphical frontend

SHOULD TRY TO GET A BACKEND RESTFUL API for GCLOUD RUN. Can just use the builtin firebase api or something. Really only need key-value stores.

## Kubernetes

Mostly only useful for microservices, large scale parallelisable compute (distributed over many, many nodes). For apps, people usually use it to set up a PaaS. So you would buy an on-premises or IaaS subscription and setup your kubernetes config. This means you will also have to let kubernetes manage the amount of compute power available given to you. Instead of letting the cloud provider automatically scale for you. This gives you more control, which would be best for very complex app management (VCAM).



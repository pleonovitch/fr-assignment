# Assignment
```
Technical Exercise:
The goal of the assignment to evaluate basic programming and cloud deployment skills. We want to see how candidates express themself in code (including test and deployment).

- Write a Python based REST style API that consumes a text file and returns a JSON object with the following
    - The longest word(s)
    - Number of words
    - Average word length
    - Count of unique words
    - Count of palindromes
- Use parallel processing if possible, for faster response
- Show a simple unit test for some part of or all the logic
- Package the service in a Docker image
- Provide Infrastructure code for deploying the service in Kubernetes on Google Cloud
- Show a simple integration test
- Create a command to do all the above : build docker, provision K8 cluster in GCP, deploy the container in K8, and run integration tests against the new deployment. The command can require a config file for any cloud credentials or other properties.
```
## Application implementation Notes
The choice has been made to implement very simple Flask based python application.
I am assuming that for the simple excercise the issues with authentication and scalability are not to be concern.
App attempts ot process text with some level of paralesim  by splitting file into chunks
and assigning processes from the pool to run "map" before reducing it.
Very simple unit tests are implemented for **is_palindrome()** and **merge_counts()** methods

For very large text processing different processing model would probably be more benefitical:
- client stores content in cloud storage, client sends requests to service 
- server is processing data using Dataflow
- asynchronous interaction also something that can be considered to eliminate client wait

## Deployment Process
__Assumptions and Limitations__:
  Prerequisites:
  - gcloud sdk is installed
  - kubectl is installed
  - j2cli is installed
  - gcloud is authed with service account that has sufficient privilegs to provision GKE, run cloud build command etc
  - terraform is installed
  - curl is installed
### Configuration
Place proper values into ``config.env`` specifying your project and zone.
Load the environment:
```
. config.env
```
Place proper values in ```config.yaml`` 
TODO: **This is duplicate** for some reason I had problems getting j2 to render environmental variables in tempaltes, not sure why.

### Manual Steps 
1. **Prepare supporting CB image that will be used for unit testing of application**
```
cd support images
gcloud builds submit --config cloudbuild.yaml .
cd ..
```

2. **Test and deploy application image**
```
cd app
gcloud builds submit --config cloudbuild.yaml .
cd ..
```

3. **Build GKE** (I am using gcloud here but normally I would do config connector deployment and wait for CR to come up)
```gcloud container clusters create $GKE_CLUSTER_NAME --num-nodes 1 --enable-basic-auth --issue-client-certificate  --zone $ZONE```

4. **Render and deploy application** TODO: prepare small HelmChart ?
```
j2 --format=yaml deployment/deployment.j2 config.yaml -o deployment/deployment.yaml
kubectl apply -f deployment/deployment.yaml 
kubectl apply -f deployment/service.yaml 
```

5. **Wait for service to become available**
```
$ kubectl get services
```

6. **Run curl transaction against service, assuming external IP is 34.122.253.69**
```
$ curl -F file=@test_data/test.txt 34.122.253.69/process
{"response":{"AVG_LENGHT":5,"LONGEST":["historiography,"],"PALINDROMS":1,"TOTAL":104,"TOTAL_LEN":622,"WORD_COUNTS":{"(singular":1,"Alexander":1,"B.C.,":2,"Black":1,"From":1,"Games.":1,"Great":1,"Greece":2,"Greek":1,"Greeks":1,"Hellenistic":1,"II":1,"India.":1,"Macedon":1,"Mediterranean":2,"Olympic":1,"Philip":1,"Sea.":1,"The":1,"Western":4,"ancient":1,"and":4,"antiquity.":1,"as":1,"being":1,"birthplace":1,"century":2,"city-states,":1,"civilization,":1,"conquering":1,"considered":1,"cradle":1,"culture":1,"democracy,":1,"drama":1,"eastern":1,"eighth":1,"fourth":1,"from":1,"height":1,"his":1,"historiography,":1,"in":2,"independent":1,"influence":1,"into":1,"is":1,"known":1,"literature,":1,"major":1,"mathematical":1,"most":1,"much":1,"of":6,"organised":1,"period":1,"philosophy,":1,"poleis":1,"polis),":1,"political":1,"present-day":1,"principles,":1,"rapidly":1,"saw":1,"science,":1,"scientific":1,"son":1,"spanned":1,"subsequent":1,"the":12,"to":1,"united":1,"various":1,"were":1,"which":1,"with":1,"world,":1}},"success":true}
```

Validation of  some key elements of JSON response against expected can give some level of confidence that application responds correctly:
```
curl -F file=@test_data/test.txt 34.122.253.69/process | jq '.response.TOTAL_LEN' > received_tl.txt
```

## Automated process of deployment
**Notes**
My preferred way of deploying infrastructure would be to have dedicated "infra" GKE cluster with config connector deployed
with further validation done with python code using k8s APIs. 

For this excerszie I will use terraform and Makefile

- Deploy:
```make deploy_app```

- Cleanup
```make clean```


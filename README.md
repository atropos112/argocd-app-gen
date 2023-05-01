# Aim

The aim of this project is to generate a yaml which is a custom resources of type `applications.argoproj.io`. This yaml should describe an application in a given repository. So that doing `kubectl apply -f thisyaml.yaml` will delpoy the application to ArgoCD which will the deploy it correctly to the cluster itself.

# Definitions
- A non-scoped namespace represents a namespace inside of kubernetes cluster, e.g. platform, monitoring, it doesn't have specific user or intent in mind.
- A scoped-namespace represents a namespace inside of a kubernetes cluster, it is assigned to a specific user or a purpose, e.g. platform-trudo being trudo's platform namespace or general-yi, being the general namespace with scope yi.
- Infrastructure folder is a folder which contains non-scoped namespaces as folders in its root directory with folders within them representing applications living in that namespace. 


# Structure Of Repository
Below I describe what repository is expected. I find that best way to describe why the structure has to be by briefly explainig what problem occured and how it was solved.

### Problem 1
In terms of structure a simplest way to go is to have a repository with folders in root directory representing non-scoped namespaces, in reality hosting the GitOps on the very infrastructure we are running on is risky, and this risk shouldn't exist for some applications.

As a result the following complication is made. A git repository may be an infrastructure folder or it can have multiple infrastructure folders in its root directory. As a result the root directory in a git repository has folders that are in fact infrastructure folders. This allows for a repository to have two folders in its root say `core` and `apps` where `core` should only be reconciled from a mirrored repository for extra safety while `apps` should be reconciled from this repository for extra speed (shorter dev loop).


### Problem 2
Once we are in an infrastructure folder how does one decide if the application should be deployed in the non-scoped namespace or scoped-namespace. You could simply have scoped-namespaces along with non-scoped namespaces in the infrastructure folder but that would lead to a lot of duplication, so thats a no.

The applications are either bunch of yamls or a helm chart. A helm chart is easily resolved by calling the overdies file `values.<scope>.yaml` where `scope=atro` is the non-scoped case while anything else deploys to a scoped-namespace. With yamls, either duplication is an issue which means it should be turned into a yaml or duplication is not an issue. If duplication is not an issue the application folder is to end with `-<scope>` to signal which scoped-namespace to deploy into, if the `-<scope>` is missing its deployed to non-scoped namespace.

# Using this repository
Start with cloning/forking it. Then locally activate pre-comit-config with

```bash
pip install pre-commit
pre-commit install
```

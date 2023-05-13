# What does it do ?

Under specific folder structure of a repository containing the application (bare yamls or helm charts) this python application generates all the corresponding `Application` custom resources for ArgoCD. It by default uses full-sync but with `ARGO_DEV_MODE=1` set sets to no sync. In addition it is possible to override default templating on application to application basis as well as changing the template for all the applications without touching any code (just `app.tpl`).

# What are the requirements ?

Before I outline what structure is expected let me introduce my definition of scoped namespace. User may or may not opt for using scoped namespaces. When I say scoped I mean you may want to have a `media` namespace and then for a friend called Bob you may want to have a separate `media-bob` namespace allowing you to keep separation but on repository level not have to duplicate code as for a helm chart all this would require is a `values.yaml` that shares settings between all instances of an application and then `values.atro.yaml` for `media` namespace and `values.bob.yaml` for `media-bob` namespace. In this case `media` is the non-scoped and `media-bob` is the scoped namespace.

The folder structure expects to start with non-scoped namespaces followed by a per application folders. If the folder is a yaml file its expected to be in the non-scoped namespace *unless* a `scope.bob` file exists (`scope.bob` would indicate this should be installed in `mynamespace-bob` namespace). If its a helm chart it is instead divided by the values overrides file, namely the values.atro.yaml represents the non-scoped namespace meanwhile values.anythingelse.yaml would represent the chart in the scoped namespace (e.g. `values.bob.yaml` would deploy a helm chart to `mynamespace.bob` namespace).

A user may have many repositories and can choose to "respect" the outlined folder structure starting from a subfolder rather than entire repository. In case user doesn't use scoped namespaces they still have to have override files called `values.atro.yaml` to indicate this is indeed meant to go to the non-scoped namespace.

## Example
platform
 -> harbor: values.yaml, values.atro.yaml, templates, Chart.yaml
 -> argocd: values.yaml, values.atro.yaml, Chart.yaml
media
 -> sonarr: values.yaml, values.atro.yaml, values.bob.yaml, Chart.yaml, templates
 -> navidrome: values.yaml, values.bob.yaml, Chart.yaml
 -> radarr: all.yaml, scope.bob
kube-system
 -> metallb: all.yaml

Would create applications for
- harbor in platform namespace (using `values.atro.yaml` overriding the `values.yaml`)
- argocd in platform namespace (same as harbor)
- sonarr in media namespace with `values.yaml -> values.atro.yaml` and in media-bob with `values.yaml -> values.bob.yaml`
- navidrome in namespace media-bob with `values.yaml -> values.bob.yaml`
- radarr in namespace media-bob with just the yamls applied as they are
- metallb in kube-system namespace with yamls applied as they are

# Using this

TO EXPLAIN.
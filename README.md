# What does it do ?

This application automatically generates `Application` custom resources for ArgoCD based on your git ops repository. In addition it is possible to override default templating on application to application basis as well as changing the template for all the applications without touching any code (just edit `app.tpl`).

# What are the requirements ?

Before I outline what structure is expected let me introduce my definition of scoped namespace. User may or may not opt for using scoped namespaces. When I say scoped I mean you may want to have a `media` namespace and then for a friend called Bob you may want to have a separate `media-bob` namespace allowing you to keep separation but on repository level not have to duplicate code as for a helm chart all this would require is a `values.yaml` that shares settings between all instances of an application and then `values.atro.yaml` for `media` namespace and `values.bob.yaml` for `media-bob` namespace. In this case `media` is the non-scoped and `media-bob` is the scoped namespace.

The folder structure expects to start with non-scoped namespaces followed by a per application folders. If the folder is a yaml file its expected to be in the non-scoped namespace *unless* a `scope.bob` file exists (`scope.bob` would indicate this should be installed in `mynamespace-bob` namespace). If its a helm chart it is instead divided by the values overrides file, namely the values.atro.yaml represents the non-scoped namespace meanwhile values.anythingelse.yaml would represent the chart in the scoped namespace (e.g. `values.bob.yaml` would deploy a helm chart to `mynamespace.bob` namespace).

A user may have many repositories and can choose to "respect" the outlined folder structure starting from a subfolder rather than entire repository. In case user doesn't use scoped namespaces they still have to have override files called `values.atro.yaml` to indicate this is indeed meant to go to the non-scoped namespace.

## Example
platform
 -> harbor: `values.yaml`, `values.atro.yaml`, `templates`, `Chart.yaml`
 -> argocd: `values.yaml`, `values.atro.yaml`, `Chart.yaml`
media
 -> sonarr: `values.yaml`, `values.atro.yaml`, `values.bob.yaml`, `Chart.yaml`, `templates`
 -> navidrome: `values.yaml`, `values.bob.yaml`, `Chart.yaml`
 -> radarr: `all.yaml`, `scope.bob`
kube-system
 -> metallb: `all.yaml`

Would create applications for
- harbor in platform namespace (using `values.atro.yaml` overriding the `values.yaml`)
- argocd in platform namespace (same as harbor)
- sonarr in media namespace with `values.yaml -> values.atro.yaml` and in media-bob with `values.yaml -> values.bob.yaml`
- navidrome in namespace media-bob with `values.yaml -> values.bob.yaml`
- radarr in namespace media-bob with just the yamls applied as they are
- metallb in kube-system namespace with yamls applied as they are

# Using this

This application is obviously opinionated but suppose you are happy with the structure requirement outlined above to use this all you have to edit it the `config.yaml` file. I leave my settings there for ease of use for myself but also to give a real example of what is needed.

Infrastructure component of the config is compulsory, its composed of a list where each element has up to 3 elements, 
- `repo_path` (required): Where the repository exists on your local device, not the folder where the structure begins, but where the git repository begins. This is the git repository's root directory.
- `repo_url` (required): The url to the git repository, ssh or https. This will be passed to ArgoCD to do the resolving.
- `infra_path` (optional): If not set its set to be equal to `repo_path`. Its where the (non-scoped) namespace folders are, its always going to be either the `repo_path` or a directory inside of the `repo_path`.

The `app.tpl` is something you may also want to edit to change the output for all applications.

To override behaviour for specific applications, first start with application name and then write a bit of yaml that you'd like to be overriden. For example if you would like to override ignore differences in metallb then 
```yaml
  metallb:
    spec:
      ignoreDifferences:
        - group: apiextensions.k8s.io
          jsonPointers:
            - /spec/conversion
          kind: CustomResourceDefinition
```
Note should you add ignore differences to `app.tpl` and here, the ones from `app.tpl` are replaced with the ones specified here (not merged into one list).

By default uses full-sync but with `ARGO_DEV_MODE=1` set sets to no sync.

Once the structure is set, `config.yaml` and `app.tpl` are adjusted simply call `python main.py`.
# I don't like how you did X I would like something different

This application is very opinionated, making it more generic is hard if not impossible because the list of assumptions needed to make this work is large. If you have an improvement suggestion please create an issue, if you would like to change it to better fit your need fork it and feel free to create an issue inquirying where to change what to accomplish what you want.
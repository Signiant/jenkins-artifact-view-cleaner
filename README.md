# jenkins-artifact-view-cleaner
Cleans artifacts from a build repo if no corresponding job exists in a Jenkins view

# Purpose
Remove stale branch artifacts from a disk repo if there is no longer a Jenkins job for the branch

# Command Line Options

* -h : displays help
* -d : enable debug output
* -r : enable dry run mode (do not remove artifacts)
* -f : base path to artifacts for a project
* -v : view name in Jenkins
* -j : Base Jenkins URL



# Usage

In the example below, note that everything after the image name (signiant/jenkins-artifact-view-cleaner) are arguments to the container *NOT* to the docker run command

```bash
docker run \
   -v /builds/Jenkins/myproject:/builds/Jenkins/myproject \
   signiant/jenkins-artifact-view-cleaner \
        -f /builds/Jenkins/myproject:/builds/Jenkins/myproject \
        -v myproject-branches \
        -j http://myjenkins.foo.com:8080 \
        -d
```

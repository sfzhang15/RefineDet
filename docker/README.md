# Refinedet standalone Dockerfiles.

The `standalone` subfolder contains docker files for generating both CPU and GPU executable images for Caffe.
Currently, only CPU executable image is confirmed to be working. GPU is supported in the future.
The images can be built using make, or by running:

```
docker build -t refindet:cpu standalone/cpu
```
for example.

# Running Refinedet using the docker image

In order to test the Refinedet image, run:
```
docker run -ti refindet:cpu caffe --version
```
which should show a message like:
```
libdc1394 error: Failed to initialize libdc1394
caffe version 1.0.0-rc3
```

One can also build and run the Caffe tests in the image using:
```
docker run -ti refindet:cpu bash -c "cd /opt/caffe; make runtest"
```

In order to get the most out of the caffe image, some more advanced `docker run` options could be used. For example, running:
```
docker run -ti --volume=$(pwd):/workspace refindet:cpu caffe train --solver=example_solver.prototxt
```
will train a network defined in the `example_solver.prototxt` file in the current directory (`$(pwd)` is maped to the container volume `/workspace` using the `--volume=` Docker flag).

Note that docker runs all commands as root by default, and thus any output files (e.g. snapshots) generated will be owned by the root user. In order to ensure that the current user is used instead, the following command can be used:
```
docker run -ti --volume=$(pwd):/workspace -u $(id -u):$(id -g) refindet:cpu caffe train --solver=example_solver.prototxt
```
where the `-u` Docker command line option runs the commands in the container as the specified user, and the shell command `id` is used to determine the user and group ID of the current user. Note that the Refinedet docker images have `/workspace` defined as the default working directory. This can be overridden using the `--workdir=` Docker command line option.

# Other use-cases

Although running the `caffe` command in the docker containers as described above serves many purposes, the container can also be used for more interactive use cases. For example, specifying `bash` as the command instead of `caffe` yields a shell that can be used for interactive tasks. (Since the caffe build requirements are included in the container, this can also be used to build and run local versions of caffe).

Another use case is to run python scripts that depend on `caffe`'s Python modules. Using the `python` command instead of `bash` or `caffe` will allow this, and an interactive interpreter can be started by running:
```
docker run -ti refindet:cpu python
```
(`ipython` is also available in the container).

Since the `caffe/python` folder is also added to the path, the utility executable scripts defined there can also be used as executables. This includes `draw_net.py`, `classify.py`, and `detect.py`


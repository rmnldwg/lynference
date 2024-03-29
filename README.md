# `lynference`

```mermaid
flowchart TD
node1["data/2021-clb-oropharynx.csv.dvc"]
node2["data/2021-usz-oropharynx.csv.dvc"]
node3["data/2023-clb-multisite.csv.dvc"]
node4["data/2023-isb-multisite.csv.dvc"]
node5["clean"]
node6["enhance"]
node7["evaluate"]
node8["filter"]
node9["join"]
node10["plot-corner"]
node11["sampling"]
node12["remote"]
node1-->node9
node1-->node12
node2-->node9
node2-->node12
node3-->node9
node3-->node12
node4-->node9
node4-->node12
node5-->node7
node5-->node11
node5-->node12
node6-->node8
node6-->node12
node7-->node12
node8-->node5
node8-->node12
node9-->node6
node9-->node12
node10-->node12
node11-->node7
node11-->node10
node11-->node12
```

We are researchers in the field of medical physics and want to predict how cancer in the head & neck region spreads through the lymphatic system.

`lynference` is a repository that allows anyone to obtain and/or reproduce the results of our research. We will use it to expose future publications to more scientific scrutiny and enable anyone to truly build upon what we have done, instead of just writing a brief _methods_ section and call it a day.

In the following we will explain, how it all works and what you have to do to obtain/reproduce our results.

## Content

- [:gear: Requirements](#gear-requirements)
- [:arrow_down: Download Data](#arrow_down-download-data)
- [:recycle: Reproduce a Pipeline](#recycle-reproduce-a-pipeline)
- [:package: Releases](#package-releases)
- [:compass: Navigating the repo](#compass-navigating-the-repo)
- [:soon: Roadmap](#soon-roadmap)
- [:envelope: Anything unclear?](#️envelope-anything-unclear)

## :gear: Requirements

![python-badge](https://img.shields.io/badge/python-3.8-blue)
![platform](https://img.shields.io/badge/platform-Ubuntu%2020%20%7C%2022-orange)

> :warning: **NOTE:** \
> We highly recommend using a virtual environment for anything that comes below. Feel free to use any tool you are comfortable with. We use [venv], and you can use these commands to get your virtual environment started:
> ```bash
> python3 -m venv .venv
> source .venv/bin/activate
> pip install --upgrade pip setuptools wheel
> ```
> using [conda] (and assuming it is installed on your machine), the same process would look like this:
> ```bash
> conda create -n yourenv python=3.8 pip setuptools wheel
> conda activate yourenv
> ```

All requirements can be installed using [pip] and the `requirements.txt` file at the root of this repository:

```bash
pip install -r requirements.txt
```

This will install these three packages and its dependencies:
* [DVC], which is a tool that allows the versioning of arbitrary data and pipelines, while keeping git uncluttered.
* [`lymph-model`]: The implementation of our mathematical model on lymphatic spread [[1]](#1)
* [`lyscripts`]: A command line interface (CLI) to perform the various steps of the pipeline. 

We should mention that any of the pipelines defined here also depend on some raw data, which is stored in a repository called [`lyDATA`] where we also explain how the data was extracted and what was recorded in it.

[![up-button]](#lynference)

## :arrow_down: Download Data

If you just want to download the data our pipelines have produced, you should be able to do that with only [DVC] installed by executing the [`dvc get`] command. Let's say you wanted to download the drawn `samples.hdf5` inside the :file_folder: `models` directory of this repo at commit `123456`. This is how to do it:

```bash
dvc get https://github.com/rmnldwg/lynference --rev 123456 models/samples.hdf5
```

> :warning: **NOTE:** \
> This does not work with the revisions [`bilateral-v1`], [`midline-with-mixing-v1`] or [`midline-without-mixing-v1`]. They precede how we now set up our remote [DVC] storage now. However, for those revisions the respective [DVC] remote storage is attached to the linked releases as a `.zip` file.

[![up-button]](#lynference)

## :recycle: Reproduce a Pipeline

[DVC] makes pipelines persistent using *pipeline files* (like the `dvc.yaml` at the root and the one inside the `pipeline` directory) that detail how [DVC] should execute various commands and how they depend on each other. After a successful run of a pipeline, [DVC] stores the MD5 hashes of all produced files in the `dvc.lock` file. This allows us to store the data - which may be binary and/or very large - to be stored elsewhere, while [DVC] will still know how to find it.

To reproduce a pipeline, follow these steps:

### 1. Clone Repository

Clone this repository, enter it and checkout the revision of the pipeline you're interested in. Usually, this would be the name of a tag:

```bash
git clone https://github.com/rmnldwg/lynference.git
cd lynference
git checkout <revision-of-interest>
```

### 2. Update requirements

We might change/update the `requirements.txt` used to install the dependencies, so it is recommended you use

```bash
pip install -r requirements.txt
```

again after checking out the `<revision-of-interest>`.

### 3. Get the raw data

Now we download the raw data that is the starting point of the pipeline. Where to get it from is already defined in the `.dvc` files inside the `data` folder. We only need to tell [DVC] to go and get them:

```bash
dvc update --recursive ./data
```

Since they are also stored in the [DVC] remote on Azure, you could also do this:

```bash
dvc get https://github.com/rmnldwg/lynference --rev <revision-of-interest> data/<dataset>.csv
```

### 4. Start the pipeline

Finally, the pipeline can be launched. If everything works as intended the command below should launch the pipeline. Note that it may take quite some time to finish (something on the order of hours). But during the entire process, it should keep you updated about what's happening.

```bash
dvc repro pipeline
```

### 5. Cleaning up

Assuming you have used [venv], all you need to do to erase the entire virtual environment, the repository, pipeline and all associated data is to deactivate the environment, leave the repository and delete it

```bash
deactivate
cd ..
rm -rf lynference
```

[![up-button]](#lynference)

## :package: Releases

If you want to see a list of pipelines we have published so far, head over to the [releases] on GitHub. Every successful run of a pipeline will be published as a release, alongside a ZIP file containing a [DVC] remote for that exact run. [Read here](https://dvc.org/doc/command-reference/remote#remote) how to use it to fetch the data from it.

The development of these pipelines might happen in dedicated `pipeline-xyz` branches, which may reflect unfinished stages of a pipeline, where parts crash or where we still figure out some parameters.

[![up-button]](#lynference)

## :compass: Navigating the repo

Here's a little overview over this repository's contents and what they do:

### :page_facing_up: `dvc.yaml` and `pipeline/dvc.yaml`

The `dvc.yaml` _inside_ the `pipeline` folder defines the commands that should be run to reproduce the pipeline. It also defines what each command depends on (input files and parameters/settings) and what it outputs. In this way, it can connect the individual stages into a _directed acyclic graph_ (DAG), which is displayed at the top for the current pipeline.

The `dvc.yaml` at the root of the repository does some additional stuff like creating a visual representation of the mentioned DAG and - more importantly - export the current python environment into a `frozen.txt` file. However, running this requires additional dependencies, and it is really only necessary, when _creating_ a pipeline.

Look at the files and the descriptions we have put at each stage to get an idea of what happens there.

> :warning: **WARNING:** \
> Leave the `dvc.lock` file unchanged, it is managed by [DVC].

### :page_facing_up: `params.yaml`

This is a configuration file that defines parameters and settings for the individual stages in the pipeline. Almost all the scripts in the [`lyscripts`] repository take a `--params` argument where this file is passed and use some keys and values defined there.

We have put extensive comments in that file that explain what each entry there does.

### :page_facing_up: `requirements.txt` and :page_facing_up: `frozen.txt`

These two text files define the Python packages necessary to run the pipeline. Note that **for reproduction**, you should **use `frozen.txt`**, as it is always created at the end of each pipeline run.

The `requirements.txt` file is only used by us during development.

### :file_folder: data

When you first clone the repository, this does not contain any data. Only two `.dvc` files. When issuing the command `dvc update` in [step 3](#3-get-the-raw-data), [DVC] sets out and tries to get the actual data from the location defined in these `.dvc` files. In this case, they are fetched from the [`lyDATA`] repository.

### :file_folder: models

During the run of the pipeline, a lot of samples and predictions are produced. Most of them are stored inside HDF5 files inside this models' folder.

Essentially, all computationally intensive results are stored here from which plots and tables can be produced.

### :file_folder: plots

This stores both data series (e.g. as CSV files) and images of plots which are created during the pipeline run. Some of them serve as checks to ensure everything went smoothly during the computations.

[![up-button]](#lynference)

## :soon: Roadmap

We are aware that there is still work to do to make this more reproducible.

For instance, we did not manage yet to make the pipeline _fully_ deterministic. E.g., it seems at least one library we use does not respect numpy's random number generator. But we _can_ guarantee that the end results are all within narrow margins, even if they are rerun from scratch.

Also, the way to set up the Python environment isn't super user-friendly yet. The gold standard is of course a docker container, but we didn't get to that yet.

[![up-button]](#lynference)

## :envelope: Anything unclear?

If there are still unanswered questions regarding this work, don't hesitate to :envelope: [contact us](mailto:roman.ludwig@usz.ch). We are happy to help and will provide you with what we can provide.

[![up-button]](#lynference)

[venv]: https://python.readthedocs.io/en/stable/library/venv.html
[pip]: https://pip.pypa.io/en/stable/
[conda]: https://docs.conda.io/en/latest/
[DVC]: https://dvc.org
[`lyDATA`]: https://github.com/rmnldwg/lydata
[`lyscripts`]: https://github.com/rmnldwg/lyscripts
[`lymph-model`]: https://github.com/rmnldwg/lymph
[`lymph`]: https://github.com/rmnldwg/lymph
[`dvc get`]: https://dvc.org/doc/command-reference/get
[`bilateral-v1`]: https://github.com/rmnldwg/lynference/releases/tags/bilateral-v1
[`midline-with-mixing-v1`]: https://github.com/rmnldwg/lynference/releases/tags/midline-with-mixing-v1
[`midline-without-mixing-v1`]: https://github.com/rmnldwg/lynference/releases/tags/midline-without-mixing-v1
[zenodo]: https://zenodo.org
[releases]: https://github.com/rmnldwg/lynference/releases

[up-button]: https://dabuttonfactory.com/button.png?t=back+to+top&f=Roboto-Bold&ts=15&tc=eef&hp=16&vp=5&c=6&bgt=unicolored&bgc=89a

## References

<a id="1">[1]</a>
Roman Ludwig, B. Pouymayou, P. Balermpas, and J. Unkelbach,
**A hidden Markov model for lymphatic tumor progression in the head and neck**,
*Sci Rep*, vol. 11, no. 1, p. 12261, Dec. 2021,
doi: https://doi.org/10.1038/s41598-021-91544-1.

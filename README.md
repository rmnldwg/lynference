
![pipeline](./dag.png)

## What is **`lynference`**?

It is a repository that aims at making our research (modelling lymphatic cancer progression in head & neck cancer) completely reproducible. It essentially stores the pipelines we have created persistently. These pipelines include the data pre-processing, inference, evaluation and prediction.

The pipelines stored here largely depend on three other repositories:

1. The [`lymph`] repository, where we develop the mathematical model in the form of a Python library. **If you want to learn more about how we model the lymphatic spread of head & neck cancer, you can find more info in this repository**
2. [`lyDATA`], a repository that makes data on the patterns of lymphatic progression publicly available. This means we publish (anonymized) patient data here that details where in their lymphatic system the respective patient had lymph node metastases. The info over there is less mathematical and more clinical.
3. A command line tool [`lyscripts`] tailored to the specific purposes and use cases within the pipelines published here.

## How to reproduce a pipeline

To define pipelines and make them persistent, we use a tool called [DVC]. Using this program, one can define a *pipeline file* (both the `dvc.yaml` at the root and the one inside the `pipeline` directory are such pipeline files) that details how [DVC] should execute various commands and how they depend on each other. After a successful run of a pipeline, [DVC] stores the MD5 hashes of all produced files in the `dvc.lock` file. This enables one to store the (large) data produced by different runs elsewhere while still having everything in version control.

The commands that [DVC] aims to chain together into a reproducible pipeline are largely commands from [`lyscripts`], which is a python package full of "convenience" methods and scripts that - in turn - use the code from our [`lymph-model`] library to perform e.g. data cleaning, inference, model comparison and predictions.

If you want to reproduce our work, then follow these steps:

### ⚠️ Note

We have only tested these pipelines on **Ubuntu** (20.04 and above, WSL2 works) and with **Python 3.8**. We cannot guarantee that any other setup works.

### 1. Repository

Clone this repository, enter it and checkout the revision of the pipeline you're interested in. Usually, this would be the name of a tag:

```bash
git clone https://github.com/rmnldwg/lynference.git
cd lynference
git checkout <revision-of-interest>
```

### 2. Virtual environment

We strongly recommend installing the necessary Python packages inside a virtual environments. Upon creating these pipelines, we were using [`venv`], which is normally pre-installed with Python. Below we'll show you how this works:

First create the virtual environment, activate it and make sure all basics are installed:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
```

You could probably also use any other virtual environment manager, like [`conda`] for which this process would look like slightly different.

Following this and regardless of the virtual environment you set up, is the time to install the requirements:

```bash
pip install -r frozen.txt
```

### 3. Get the raw data

Now we download the raw data that is the starting point of the pipeline. Where to get it from is already defined in the `.dvc` files inside the `data` folder. We only need to tell [DVC] to o and get them:

```bash
dvc update --recursive ./data
```

### 4. Start the pipeline

Finally, the pipeline can be launched. If everything works as intended the command below should launch the pipeline. Note that it may take quite some time to finish (something on the order of hours). But during the entire process, it should keep you updated about what's happending.

```bash
dvc repro pipeline
```

### 5. Cleaning up

Assuming you have used [`venv`], all you need to do to erase the entire virtual environment, the reporitory, pipeline and all associated data is to leave the repository

```bash
cd ..
```

and then delete it

```bash
rm -rf lynference
```

## Branching model

On our `main` branch we aim to always only publish tagged, working and reproducible pipelines and create [releases] from them, which may at some point also be stored on platforms like [zenodo] to make them citeable and even more persistent.

So, if you want to see a list of pipelines we have published so far, head over to the [releases] on GitHub. Every run of a pipeline will be published as a release, alongside a ZIP file containing a [DVC] remote for that exact run.

The development of these pipelines happens in dedicated `pipeline-xyz` branches, which might reflect unfinished stages of a pipeline, where parts crash or where we still figure out some parameters.

## Navigating the repo

Here's a little overview over this repository's contents and what they do:

### 📄 `dvc.yaml` and `pipeline/dvc.yaml`

The `dvc.yaml` _inside_ the `pipeline` folder defines the commands that should be run to reproduce the pipeline. It also defines what each command depends on (input files and parameters/settings) and what it outputs. In this way, it can connect the individual stages into a _directed acyclic graph_ (DAG), which is displayed at the top for the current pipeline.

The `dvc.yaml` at the root of the repository does some additional stuff like creating a visual representation of the mentiond DAG and - more importantly - export the current python environment into a `frozen.txt` file. However, running this requires additional dependencies and it is reallz onlz necessarz, when _creating_ a pipeline.

Look at the files and the desciptions we have put at each stage to get an idea of what happens there.

⚠️ **Warning:** Leave the `dvc.lock` file unchanged, it is managed by [DVC].

### 📄 `params.yaml`

This is a configuration file that defines parameters and settings for the individual stages in the pipeline. Almost all the scripts in the [`lyscripts`] repository take a `--params` argument where this file is passed and use some keys and values defined there.

We have put extensive comments in that file that explain what each entry there does.

### 📄 `requirements.txt` and 📄 `frozen.txt`

These two text files define the Python packages necessary to run the pipeline. Note that **for reproduction**, you should **use `frozen.txt`**, as it is always created at the end of each pipeline run.

The `requirements.txt` file is only used by us during development.

### 📁 data

When you first clone the repository, this does not contain any data. Only two `.dvc` files. The command `dvc update <path-to-file>` [DVC] sets out and tries to get the actual data from the location defined in these `.dvc` files. In this case, they are fetched from the [`lyDATA`] repository.

### 📁 models

During the run of the pipeline, a lot of samples and predictions are produced. Most of them are stored inside HDF5 files inside this models folder.

Essentially, all computationally intensive results are stored here from which plots and tables can be produced.

### 📁 plots

This stores both data series (e.g. as CSV files) and images of plots which are created during the pipeline run. Some of them serve as checks to ensure everything went smoothly during the computations.

## Anything unclear?

If there are still unanswered questions regarding this work, don't hesitate to 📧 [contact us](mailto:roman.ludwig@usz.ch). We are happy to help and will provide you with what we can provide.


[`lyDATA`]: https://github.com/rmnldwg/lydata
[`lyscripts`]: https://github.com/rmnldwg/lyscripts
[`lymph-model`]: https://github.com/rmnldwg/lymph
[`lymph`]: https://github.com/rmnldwg/lymph
[DVC]: https://dvc.org
[`venv`]: https://docs.python.org/3/library/venv.html
[`conda`]: https://docs.conda.io/en/latest/index.html
[zenodo]: https://zenodo.org
[releases]: https://github.com/rmnldwg/lynference/releases

"""
Compute the probability of midline extension for the drawn samples.
"""
import argparse
from pathlib import Path

import numpy as np
import scipy as sp
from emcee.backends import HDFBackend
import json

from lyscripts.utils import load_yaml_params, create_model_from_config


THIN = 10


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-p", "--params", type=Path, default="params.yaml",
        help="Path to the parameter file."
    )
    parser.add_argument(
        "-m", "--metrics", type=Path, default="midext_ratios.json",
        help="Path to the output metrics file."
    )
    args = parser.parse_args()

    # Load the parameters
    params = load_yaml_params(args.params)
    first_binom_prob = params["model"]["first_binom_prob"]
    max_t = params["model"]["max_t"]
    time = np.arange(max_t + 1)

    # create the model
    model = create_model_from_config(params)
    num_spread_probs = len(model.spread_probs)

    # Initialize the metrics
    midext_ratios = {stage: [] for stage in params["model"]["t_stages"]}

    # Load the samples
    backend = HDFBackend(params["general"]["samples"], read_only=True)
    samples = backend.get_chain(thin=THIN, flat=True)

    for sample in samples:
        for i, stage in enumerate(params["model"]["t_stages"]):
            midext_prob = sample[num_spread_probs - 1]
            midext_ratios[stage].append(1. - midext_prob)

    # Compute the mean and std
    for stage in params["model"]["t_stages"]:
        midext_ratios[stage] = {
            "mean": np.mean(midext_ratios[stage]),
            "std": np.std(midext_ratios[stage])
        }

    # Write the metrics
    with open(args.metrics, "w") as f:
        json.dump(midext_ratios, f, indent=4)

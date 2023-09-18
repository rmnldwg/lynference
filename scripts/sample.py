"""
Draw samples and perform a thermodynamic integration for the new version (1.0.0.a2)
of the code.
"""
import argparse
import logging
from pathlib import Path
import lymph

import emcee
from lyscripts.utils import (
    load_yaml_params,
    graph_from_config,
    binom_pmf,
)
import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


def parametric_binom_pmf(support: np.ndarray, p: float) -> np.ndarray:
    """Return the binomial pmf for a range of values of `n`."""
    return binom_pmf(k=support, n=support[-1], p=p)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--params", type=Path, default="params.yaml",
        help="Path to the YAML parameters file."
    )
    parser.add_argument(
        "--data", type=Path, default="data/cleaned.csv",
        help="Path to the data CSV file."
    )
    parser.add_argument(
        "--modalities", nargs="+", default=["max_llh"],
        help="Diagnostic modalities to load from YAML parameters file.",
    )
    args = parser.parse_args()

    params = load_yaml_params(args.params, logger=logger)
    graph = graph_from_config(params["graph"])
    max_time = params["model"]["max_t"]
    support = np.arange(max_time + 1)
    first_binom_prob = params["model"]["first_binom_prob"]

    if params["model"]["class"] == "Unilateral":
        model = lymph.models.Unilateral.binary(graph, max_time=max_time)
        logger.info(f"Created Unilateral model: {model}")

    else:
        raise ValueError(f"Unknown model class: {params['model']['class']}")

    for i, t_stage in enumerate(params["model"]["t_stages"]):
        if i == 0:
            model.diag_time_dists[t_stage] = binom_pmf(
                k=support, n=support[-1], p=first_binom_prob
            )
        else:
            model.diag_time_dists[t_stage] = parametric_binom_pmf
    logger.info(f"Loaded diagnose time distributions: {model.diag_time_dists.keys()}")

    model.modalities = {
        modality: spec_sens for modality, spec_sens in params["modalities"].items()
        if modality in args.modalities
    }
    logger.info(f"Loaded modalities: {model.modalities.keys()}")

    patient_data = pd.read_csv(args.data, header=[0,1,2])
    model.load_patient_data(patient_data, side="ipsi")
    logger.info(f"Added {len(model.patient_data)} patients to model.")

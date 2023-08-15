"""
Create a corner plot of the samples.
"""
import argparse
from pathlib import Path

from emcee.backends import HDFBackend
import corner

from lyscripts.plot.utils import save_figure
from lyscripts.utils import load_yaml_params, model_from_config


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-s", "--samples", type=Path, default="models/samples.hdf5",
        help="Path to samples file"
    )
    parser.add_argument(
        "-o", "--output", type=Path, default="plots/corner.svg",
    )
    args = parser.parse_args()

    backend = HDFBackend(args.samples, read_only=True)
    samples = backend.get_chain(flat=True)
    fig = corner.corner(samples)

    save_figure(figure=fig, file_path=args.output, formats=["png", "svg"])

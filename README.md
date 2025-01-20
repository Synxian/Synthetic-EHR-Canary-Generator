# Synthetic EHR Canary Generator

## Usage

To install the environment and interact with the environment execute:

```bash
pipenv install #first install
pipenv shell #open environment console
```

More info in [pipenv page](https://pipenv.pypa.io/en/latest/)

## Instructions

You must create a ```.env``` file, with the contents of ```.env.template```

Args:

- --output_dir, -o: Directory to save generated canaries.
- --dataset, -d: The reference dataset for canary generation. For custom datasets new functions may be needed.
- --input_file, -i: JSON file for the canaries options. For custom dataset new functions may be needed.
- --temperature, -t: Model temperature.
- --mode, -m: Mode for the canaries generation.
        Single is for single entries.
        History is to generate a thread of connected medical visits for each set of tags.
- --n_samples, n: How many canaries for each set of tags to make.
        If mode is single, it will generate single n_samples for each set of tags.
        If mode is history, it will generate an history composed of n_samples for each set of tags.

## Data Sources

### Meddocan

This project uses samples from [SPACCC_MEDDOCAN: Spanish Clinical Case Corpus - Medical Document Anonymization](https://github.com/PlanTL-GOB-ES/SPACCC_MEDDOCAN).

License: [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/)

Copyright (c) 2019 Secretaría de Estado para el Avance Digital (SEAD)

The dataset is used under the terms of CC BY 4.0, which allows sharing and adaptation with
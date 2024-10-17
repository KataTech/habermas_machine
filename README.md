# habermas_machine - Habermas Machine dataset

This repository contains the Habermas Machine dataset, used in
[Tessler, M. H.<sup>\*</sup>, Bakker, M. A.<sup>\*</sup>, Jarret, D., Sheahan, H., Chadwick, M. J., Koster, R., Evans, G., Campbell-Gillingham, L., Collins, T., Parkes, D. C., Botvinick, M., & Summerfield C. (2024). "AI can help humans find common ground in democratic deliberation".]()
to train and evaluate the Habermas Machine.


## Download data files from Google Cloud Storage

You can download the data from [Google Cloud Storage](https://console.cloud.google.com/storage/browser/habermas_machine).


## Load into python

You can load the data into a python colab using the following:

```
import io
import requests
import pandas as pd

file_location = (
    'https://storage.googleapis.com/habermas_machine/datasets/hm_all_candidate_comparisons.parquet'
)
response = requests.get(file_location)
with io.BytesIO(response.content) as f:
  df = pd.read_parquet(f)
```

## Coming soon...

- Colab to implement basic preprocessing done in the paper

## License and disclaimer

Copyright 2024 DeepMind Technologies Limited

All software is licensed under the Apache License, Version 2.0 (Apache 2.0);
you may not use this file except in compliance with the Apache 2.0 license.
You may obtain a copy of the Apache 2.0 license at:
https://www.apache.org/licenses/LICENSE-2.0

All other materials are licensed under the Creative Commons Attribution 4.0
International License (CC-BY). You may obtain a copy of the CC-BY license at:
https://creativecommons.org/licenses/by/4.0/legalcode

Unless required by applicable law or agreed to in writing, all software and
materials distributed here under the Apache 2.0 or CC-BY licenses are
distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the licenses for the specific language governing
permissions and limitations under those licenses.

This is not an official Google product.

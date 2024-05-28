# framebank_pipeline

This repository contains developments that appeared as a result of working on my term paper on the "Automatic Generation of Frame Information for the Russian Language Using Pre-trained Language Models". It consists of two parts:

1. The `exp` folder contains complete data from all the experiments that were discussed in the text of the term paper. The folder for each experiment has the same structure and contains text files with a prompt for the language model, training and test data, model responses, and a spreadsheet with scores for each component of automatically generated annotations for each frame.
2. The `framebank_pipeline` folder contains code to automatically generate a frame dictionary from the FrameBank database using our best algorithm, which generates each annotation component independently of the others.

## Как использовать framebank_pipeline

1. In addition to the dictionary of constructions of the FrameBank itself in tabular form, a table is needed in which lexemes are compared with English-language frames from FrameNet (see `framebank_pipeline/data` for examples). There you can also obtain a frequency dictionary, which is used to select examples.
2. Run `scripts/data_preparation.py` to prepare the data for generation. Tokens will be grouped into frames, the optimal main example will be selected for each, and information from the English-language FrameNet will be added to the data. You can obtain the prepaired data in `data` folder.
3. Specify your OpenAI API key in `generation_pipeline/generator.py`.
4. Now you are ready to create a frame dictionary! Run `generate_frames.py`. The file with the generated frame annotations will appear in the `data` folder.
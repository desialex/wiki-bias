# wiki-bias
This repository contains the code used in ... for the creation of three datasets for the task of bias detection.

## Prerequisites
- Python 3.6 or later
- All dependencies `pip install -r /path/to/requirements.txt`

## Usage

#### 1. URLs
Extract the urls of all parts of the complete page edit history dump.
While dumps of small Wikipedias (like the one in Bulgarian) come in a single file,
the large ones (English, French, etc.) are split into multiple smaller files.

Make sure to select an __existing date__ from the list on
`https://dumps.wikimedia.org/{lang}wiki/` and then verify the presence of a dump called __All pages with complete page edit history__.

```bash
python url_extractor.py -o <outputfile> --lang <XX> --date <YYYMMDD>
#python url_extractor.py -o urls.txt -l fr -d 20191001
```

#### 2. Download and extraction of revision pairs
Download all parts of the dump and extract the relevant revision pairs.

__Attention!__ The download and _on-the-fly_ processing of highly compressed dump files
requires time. Consider parallelizing this step if you need to process large Wikis split
into multiple files.
```bash
python filter.py -i <inputfile> -o <outputfile> --lang <XX>
#python filter.py -i urls.txt -o revisions.txt -l fr
```

#### 3. Preprocessing and diff check
Preprocessing, segmentation, cleanup, diff check, filtering.
```bash
python diff.py -i <inputfile> -o <outputfile> --lang <XX>
#python diff.py -i revisions.txt -o diffs.pickle -l fr
```

#### 4. Sentence extraction
Sentence extraction, duplicates cleanup, classes, balancing.
```bash
python sents.py -i <inputfile> -o <outputfile>
#python sents.py -i diffs.pickle -o sents.pickle
```

#### 5. Labeling and splitting
Class labels, dataset split.
```bash
python dataset.py -i <inputfile> -l <lang> (-p <prefix>)
#python dataset.py -i sents.pickle -l fr -p __label__
```

## Datasets
Balanced and split datasets in Bulgarian, French and English (extracted from dumps `20190401`) can be found in `/datasets/`

## Citation

```
@InProceedings{aleksandrovamultilingual,
  author = "Aleksandrova, Desislava
		    and Lareau, Fran{\c{c}}ois
		    and M{\'e}nard, Pierre-Andr{\'e}}",
  title = "Multilingual Sentence-Level Bias Detection in Wikipedia",
  booktitle = "Proceedings of the International Conference Recent Advances in Natural Language Processing (RANLP 2019)",
  year = "2019",
  publisher = "Association for Computational Linguistics",
  pages = "42--51",
  location = "Varna, Bulgaria"
}
```

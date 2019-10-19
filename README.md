# wiki-staging

1. [ ] __Makefile / pipeline.sh / parallel.sh__  _# Download and process dump_
    * [ ] __filter.py__  _# Filters the XML down to articles (namespace = 0)_
    * [ ] __pov.py__  _# Filters the XML articles down to those with removed POV tags_
2. [x] __diff.py__  _# Preprocessing, segmentation, cleanup, diff check, filtering_ <br>
`python diff.py <lng> <input-file> <output-file>`
3. [x] __sents.py__  _# Sentence extraction, duplicates cleanup, classes, balancing_ <br>
`python sents.py <input-file> <output-file>`
4. [x] __dataset.py__  _# Class labels, dataset split_ <br>
`python dataset.py <input-file> <output-dir> <lng> <classifier>`

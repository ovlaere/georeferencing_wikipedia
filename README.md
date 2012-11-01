georeferencing_wikipedia
========================

This project contains a simple Python script that is capable of converting raw Wikipedia xml data into plain text by removing the Wikipedia specific markup.

The contents of this project are:
* parse_wikipedia.py - The actual script
* data/raw_wikipedia.tar.gz - A compressed version of the raw Wikipedia XML used for our research paper
* data/testfile.tar.gz - A compressed version of the resulting testfile for our research paper

### Example usage of this script
  
    ./parse_wikipedia.py data/raw_wikipedia.xml testfile

### Test set

The testfile contains 21 839 Wikipedia documents annotated with geographical coordinates that are located within a bounding box of the United Kingdom. This set of documents was constructed consist of only entities that can be considered as a certain location or spot.

### Questions

In case you have any questions, feel free to contact me.

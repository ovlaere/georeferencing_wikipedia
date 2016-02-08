georeferencing_wikipedia
========================

This project contains a simple Python script that is capable of converting raw Wikipedia XML data into plain text by removing the Wikipedia specific markup, as well as the datasets used for the ACM TOIS paper [Georeferencing Wikipedia documents using data from social media sources][wiki_paper] by Olivier Van Laere, Steven Schockaert, Vlad Tanasescu, Bart Dhoedt and Chris Jones. If you use these datasets in your research, please refer to this paper.

The contents of this project are:

* `parse_wikipedia.py` - Script to parse Wikipedia XML
* `data/raw_wikipedia.tar.gz` - A compressed version of the raw Wikipedia XML
* `data/testfile.tar.gz` - A compressed version of the resulting testfile
* `data/data_test.txt.bz2` - A compressed version of the test set of 21839 Wikipedia documents
* `data_training_full.txt.bz2` - A compressed version of the original training set of 390574 Wikipedia documents
* `data_training_filtered.txt.bz2` - A compressed version of the filtered training set of 376110 Wikipedia documents

Due to file size limitations on Github, the last three files are linked.

### Example usage of the XML parsing script
  
    ./parse_wikipedia.py data/raw_wikipedia.xml testfile

### Data sets

#### `data/testfile`

The testfile contains 21839 Wikipedia documents annotated with geographical coordinates that are located within a bounding box of the United Kingdom. This set of documents was constructed to contain only entities that can be considered as a certain location or spot.

#### `data/data_test.txt`

[Download `data/data_test.txt`](http://van-laere.net/datasets/data_test.txt.bz2)

The test set from the previous paragraph, translated to Flickr tags as described in section 3.2 ("The Wikipedia spot training and test set") on page 7 of our [research paper][wiki_paper]. Note that this file contains the line count on the first line of the file.

#### `data_training_full.txt`

[Download `data_training_full.txt`](http://van-laere.net/datasets/data_training_full.txt.bz2)

The **full** training set as described in section 3.2 ("The Wikipedia spot training and test set") on page 7 of our [research paper][wiki_paper], translated to Flickr tags. This training set is the original training set from the work of Wing and Baldridge and contains 390574 training documents. Note that this file also contains the line count on the first line of the file.

#### `data_training_filtered.txt`

[Download `data_training_filtered.txt`](http://van-laere.net/datasets/data_training_filtered.txt.bz2)

The **filtered** training set as described in section 3.2 ("The Wikipedia spot training and test set") on page 7 of our [research paper][wiki_paper], translated to Flickr tags. This training reflects the training set from the work of Wing and Baldridge, less the training items that show up in the test set we constructed in the paper. This file contains 376110 training documents and has the line count on the first line of the file.

### Questions

In case you have any questions, feel free to contact me.

### Acknowledgements

Thanks to Daniel Ferrés for following up on making the datasets available for future work.

[wiki_paper]: http://www.van-laere.net/papers/ACM_TOIS.pdf "Georeferencing Wikipedia documents using data from social media sources"


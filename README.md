ADM HW2
===

### Michele Ferraro - 1717025

The homework's solution is contained in the `main.ipynb` notebook.

It contains two sections, accounting for research and theoretical questions.

The implementation assumes the development environment to be set up using [Poetry](https://python-poetry.org/) and that data is stored in a `data` folder.

The repo also contains other Python files, containing support code not directly related to the RQs:

- `constants.py` file contains the constants used in the notebook;
- `convert_dataset.py` removes some columns from the dataset to try and make it smaller;
- `utils.py` contains all the support classes and methods called in the notebook.

#### Data processing

The research questions are run on the whole dataset (including bonuses). 

The complete dataset was too big to be loaded in memory at once. Several solutions have been tried:
- Loading only the necessary columns for each task:
 
  The high number of entries caused this solution to be impractical. Even trying to load a subset of columns did not allow my hardware to load all entries at once.
  
  Even if it were possible, loading the whole dataset at once is an effort I did not want to pursue further since it's rarely achievable in production environments.

- Use batching: `pandas`'s API allows for batch processing 
 
  Batching lets the user process the data in chunks. This solves scaling issues but is not always applicable depending on the concrete use-case.
  
  While in the homework it may have been a smart approach, it would still have required to write code to merge the results extracted from individual batches.
  
  Unfortunately, `pandas` does not natively offers support for managing really big dataset, as its API is designed to have all the dataset in memory and indexed.
  
  Other libraries (e.g. `dask`) may extend `pandas` to solve this issue, but oftentimes do so at the cost of not implementing all its API.
  
- Implement a custom processing layer

  Coming from a CS background, this is the solution I chose. I first filtered some unused fields from the script to improve processing performance, then designed a small object-oriented framework to process entries.
  
  In particular, `convert_dataset.py` contains a script to filter out some columns, most notably the `review` field which isn't used in any research question and takes a good chuck of the files' size by itself.
  
  A class to represent reviews has written, parsing the reduced fields set and supplying some default values where they're missing. Finally, a custom class is implemented `DatasetIterator` that takes care of calling an arbitrary function on each review object, hiding the placeholder tasks of loading, parsing and iterating the dataset file(s).
  
  The solutions to the RQs show a pattern similar to `split-apply-combine`, although it uses raw Python variables and structures to accumulate processing results. In a production environment, I'd consider either using a proper tool to manage data of this size (we may still optimize and fit the HW's files in memory, but real-world data may easily be much bigger anyway), such as Hadoop, or at least implement proper `Counter`, `Accumulator` and `Predicate` classes/utilities to abstract the most common tasks of optionally counting entries or computing mathematical functions on some of their fields.   
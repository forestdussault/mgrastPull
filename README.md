# mgrastPull

This script makes use of the *mg-download.py* script available through MG-RAST-TOOLS.
It will download a provided list of MG-RAST metagenome IDs, gzip all retrieved **.fastq** files,
then delete any extraneous files.

##### Example Usage
`$ python2 mgrastPull.py list_of_ids.txt /path/to/download/folder/ /path/to/MG-RAST-TOOLS`

##### Parameters

`raw_list_of_ids`: path to .txt file with IDs targeted for download

`root_path`: path to store downloaded files

`mg_rast_tools`: path to cloned MG-RAST-TOOLS repository i.e.
*/home/dussaultf/PycharmProjects/MG-RAST-Tools*

##### Input File Example
The dataset file should have each ID on a newline.

Example: *datasets.txt*
```
4580694.3
4580695.3
4580696.3
4580697.3
```

##### Requirements

 https://github.com/MG-RAST/MG-RAST-Tools
  - Python>=2.7 (*MG-RAST-Tools does not support Python3*)
  - prettytable
  - requests
  - requests_toolbelt
  - scipy
  - numpy
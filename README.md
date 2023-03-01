To use these scripts:
* Open the corresponding qzv file with the rarefaction curve
* Extract the corresponding csv and jsonp files (those corresponding to the index you want to know about)
* Run the following:

## From the jsonp file
```
python get_rarefaction_data.py --jsonp {JSONP_FILE} --out-prefix {NAME OF THE OUTFILE, TSV EXTENSION WILL BE ADDED}
```
## From the csv file, with median, and with mean
```
python get_rarefaction_data_from_csv.py --csv {CSV_FILE} --method median --out-prefix {NAME OF THE OUTFILE, TSV EXTENSION WILL BE ADDED}
python get_rarefaction_data_from_csv.py --csv {CSV_FILE} --method mean --out-prefix {NAME OF THE OUTFILE, TSV EXTENSION WILL BE ADDED}
```
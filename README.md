This project is to build and test my personal SQL database skill. 


Documentation
-------------
The purpose of this project is to build a informative summary using logs. 
The log_analysis.py script will generate three outputs:
* The most popular three articles of all time
* Most popular article authors of all time
* Days that has more than 1% of requests lead to errors


Installation 
-------------

Building the DB

Run the PSQL command to import data

```shell
psql -d news -f newsdata.sql
```

To Run the report

```shell
python log_analysis.py
```

Supported Python Version
-------------------------

Python 2.7# Udacity-FSND-LOG-ANALYSIS
# Udacity-FSND-LOG-ANALYSIS

# AAF Query Engine

 [[_TOC_]] 

## Introduction 
This is a ADO repo for AAF SQL Query package for MSSQL and Oracle. 

The first argument decides are running the assessment against Oracle or MS SQL Server. The data for the argument values is read from Azure Keyvault defined in Azure
variable groups. The arguments are read etiher from Azure keyvaul or Azure Pipleine variables depending on the nature of the argumen – secret or not secret.

- ```-dbEngine ORACLE|MSSQL```
-  ```-perfStatAuth $(perfAssessAuth)```
- ``` -perfStatPwd $(perfStatPwd)```
- ```-oraAssessUser $(oraAssessUser)```
- ```-oraAssessPwd $(oraAssessPwd)```
- ```-sqlAssessUser $(sqlAssessUser)```
- ```-sqlAssessPwd $(sqlAssessPwd)```
- ```-sqlInvReader $(sqlReader)```
- ```-sqlInvReaderPwd $(sqlReaderPwd)```
- ```-sqlInvServer $(sqlFqdnName)```
- ```-sqlInvDb $(tenantDB)```
- ```-sqlInvSch "dbo"```
- ```-sqlInvTbl "artemis-inventory"```

The first argument decides are running the assessment against Oracle or MS SQL Server. The data for the argument values is read from Azure Keyvault defined in Azure
variable groups. The arguments are read etiher from Azure keyvaul or Azure Pipleine variables depending on the nature of the argumen – secret or not secret.

## Collect stats
```collect_db_stats.py``` runs sql queries provided in files either under sql-query-package or oracle-query-package directories
depending on engine queries are run against. Both directories should have all the sql queries in separate file per query
as well as file named query_files.txt having the names of each query file to run.

Both of the options ORACLE or MSSQL runs each query it reads from above defined files and stores the results locally as csv file under
```adf/[ENGINE]/[query_file_name]``` where ENGINE is either MSSQL or ORACLE and query_file_name name of the query which
was run. The output will be stored under the directory and named as [query_file_name]-YYYY-MM-DD-HH.MM.SS.sss.csv.

```collect_db_stats.py``` is dependent on following helper module under modules directory:

- ```file_utils.py```
- ```blob_utils.py```
- ```env_utils.py```

The source database information is read MS SQL Server database defined Azure Variable Group.
This is what we call inventory database. It has a ```table aaf-inventory``` which lists the
servers to be assessed. 

## Copy to Azure
Once queries are run and results stored locally on disk, the files will be copied to Azure Blob defined in Azure Variable Groups on
AZURE_STORAGE_CONNECTION_STRING parameter. Each csv file will be copied to Azure Storage Account
under container [query_file_name] as file  [query_file_name]-YYYY-MM-DD-HH.MM.SS.sss.csv. If container does not exist,
the utility will create it.

## Usage
Check contents of the below yml files for examples on howto orchestrate running the utility through Azure Pipleines:
- ```collect-mssql_db_stats.yml```
- ```collect-oracle-stats.yml```

## Prerequisites
- Linux: Ubuntu 20.04 or higher / RHEL 8.6 or higher
- Python. 3.9.x or higher with following modules:
    - azure-storage-blob
    - pandas
    - psycopg2-binary
    - pymssql
    - sqlalchemy
    - azure-identity
    - azure-keyvault-secrets
    - cx_oracle
- Git 2.x or higher
- Oracle drivers (instantclient) 21.10 or higher
## TODO
- Add DataDog monitoring for logging.

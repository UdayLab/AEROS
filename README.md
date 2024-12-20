# 1. Prerequisites

1. Linux Operating System (E.g., Ubuntu)
2. [PostGres and PostGIS](https://www.paulshapley.com/2022/12/install-postresql-14-and-postgis-3-on.html)
3. Python 3.10 or above
4. Psycopg2 and alive_progress Python Package
    ```shell
    pip install psycopg2-binary alive_progress
    ```
5. Google Maps API key
6. [Data](https://1drv.ms/f/s!Ar09XhBKBP2MkvwTfy-AHGe3yEV1Ug?e=yPJW7g)

# 2. Setting up the database

1. Create a database in postgres to store the air pollution data.
    ```sql
    Create database soramame
    ```
        
2. Connect to the database
    ```sql
    \c soramame
    ```
3. Enable PostGIS extension to the database (admin privileges are needed)
    ```sql
    create extension postgis
    ```
4. Create a table to store the location information of the sensors. 
    ```sql
    CREATE TABLE station_info(stationid varchar not null primary key, name varchar, address varchar, location geography(POINT,4326));
    ``` 
5. Create a table to store the hourly observations of the sensors on a daily basis.
    ```sql
    create table hourly_observations(stationid varchar not null, obsDate timestamp, SO2 double precision, no double precision, no2 double precision, nox double precision, co double precision, ox double precision, nmhc double precision, ch4 double precision, thc double precision, spm double precision, pm25 double precision, sp double precision, wd varchar, ws double precision, temp double precision, hum double precision, constraint SOH unique (stationID,obsDate));
    ```
__Note:__ 
   - Do not establish primary key and foreign key relation for stationid attribute in station_info and hourly_observations tables
   - Constraint SOH unique (stationID,obsDate) is used to prevent data repetition. A sensor cannot have multiple transactions with the same timestamp.

6. __[Optional Steps:]__ We recommend it for the users who are not familar with the concepts of PostGres

   - Create a user to work with this data
        ```sql
        CREATE USER aeros WITH PASSWORD 'aeros123';
        ```
   - Grant access for the new user to work on this data
        ```sql
        GRANT CONNECT ON DATABASE soramame TO aeros;
        ```
   - Grant permission to read and write data in the tables of the database
        ```sql
        GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA public TO aeros;
        ```
9. Exit from the Postgres database.
    ```console
    control + D
    ```
# 3. Gathering the spatial location information of the stations

1. Visit the sensors location page in [AEROS website](https://soramame.env.go.jp/station)
2. Copy the first three columns (stationID, stationName, stationAddress) of all the stations and store them in an excel file.
3. Carefully convert (or export) the Excel file into a csv file named 'rawStationsInfo.csv'.
4. Execute the below Python program that reads the address of each sensors and derives the spatial location.
```shell
python3 address2LatLong.py rawStationsInfo.csv  finalStationsInfo.csv   <googleMaps API key>
```
       

# 4. Storing the information of the stations in the database

1. Open the Python file 'insertStationInfoInDatabase.py'
    ```shell
    vi insertStationInfoInDatabase.py
    ```
2. Go to the following line:
    ```python 
    conn = psycopg2.connect(database="soramame", user="", password="", host="", port=5432)
    ```
3. Specify the appropriate database, user, password, host ipaddress of postgres, and port number.
    ```python
    conn = psycopg2.connect(database="soramame", user="aeros", password="aeros123", host="163.143.165.136", port=5432)
    ```
4. Save the file and exit.
    ```console
    :wq
    ```
5. Execute the following command to store the station information into the database.
    ```shell
    python3 insertStationInfoInDatabase.py finalStationsInfo.csv
    ```
# 5. Storing hourly observation data in the database

## 5.1. Storing recent (or new) hourly data
### 5.1.1. Download the hourly data
1. Visit the download page of [AEROS website](https://soramame.env.go.jp/download)
2. In the first dropdown menu choose any month other than current month. For example, if the current month is November, choose any previous months, such as August and September.
3. In the second dropdown menu choose the default option, which is 'nationwide'.
4. Click the download button.
5. A zip file named 'data.zip' will be downloaded onto your local computer. 
6. Create a folder 'hourlyData'
```shell
mkdir hourlyData
```
7. Unzip the data.zip file by saving its contents in hourlyData folder.
```shell
unzip -d hourlyData ~/Downloads/data.zip
```
      
8. __[Optional]__ If you have multiple zips representing various months, perform this two steps.
   
   - Enter into the hourlyData directory
        ```shell
        cd hourlyData
        ```
   - Create a shell script file using the following command
     ```shell
     vi uncompressNewZipFiles.sh
     ```   
   - Copy the below provided shell script code and paste it in the above file
        ```shell
        #add the below provided code
        zipFiles=`ls *.zip` 
        for eachZipFile in $zipFiles
        do
           unzip $eachZipFile
           rm $eachZipFile
        done  
        ```
   - Execute the shell script
     ```shell  
     sh uncompressNewZipFiles.sh
     ```
   - remove the shell script file
     ```shell
     rm -rf uncompressNewZipFiles.sh
     ```
9. Delete or rename the zip file to yyyymm_00.zip for backup. 
    ```shell
        #format: mv data.zip yyyymmdd_00.zip
        mv data.zip 20240101_00.zip
    ```
10. Move back to the parent directory
    ```shell
    cd ..
    ```
### 5.1.2. Inserting the new hourly data into the database.
1. Open the Python file 'insertNewHourlyObservationsData.py'
    ```shell
    vi insertNewHourlyObservationsData.py
    ```
2. Go to the following line:
    ```python
    conn = psycopg2.connect(database="", user="", password="", host="", port=5432)
    ```
3. Specify the appropriate database, user, password, host ipaddress of postgres, and port number.
    ```python
    conn = psycopg2.connect(database="soramame", user="aeros", password="aeros123", host="163.143.165.136", port=5432)
    ```
4. Save the file and exit.

9. Run the Python program 'insertNewHourlyObservationsData.py' by specifying the folder.
    ```shell
    python3 insertNewHourlyObservationsData.py ./hourlyData
    ```
## 5.2. Storing old hourly data 
Duration of the data: 2018-01-01 to 2021-03-31

### 5.2.1. Downloading the dld zip files [Truncated]
1. Visit the download page of [AEROS website](https://soramame.env.go.jp/download)
2. In the first dropdown menu choose any month other than current month. For example, if the current month is November, choose any previous months, such as August and September.
3. In the second dropdown menu choose the default option, which is 'nationwide'.
4. Click the download button.
5. A zip file named 'data.zip' will be downloaded onto your local computer. 

### 5.2.2. Unzipping the downloaded zip files
1. Create a temporary directory, say _temp_.
    ```shell
    mkdir temp
    ```       
2. Move or upload the zip files into the _temp_ directory.
3. Enter into the temp directory
    ```shell
    cd temp
    ```
4. Create a shell script file to read every zip file and uncompress it.
    ```shell
    vi uncompressOldZipFiles.sh
    ```
5. Copy and paste the following shell script 
    ```shell       
    #add the below provided code
    zipFiles=`ls *.zip`
    
    for eachZipFile in $zipFiles
    do
      unzip $eachZipFile
      rm $eachZipFile
    done
        
    subZipFiles=`ls *.zip`
    for eachZipfile in $subZipFiles
    do
          echo 'unzipping ' $eachZipfile
          unzip $eachZipfile
          rm -rf $eachZipfile
    done
    ```
6. Execute the shell script.  
    ```shell
    sh uncompressOldZipFiles.sh
    ```
    The above program will create the folders '01' to '47'. Each folder represents a Prefecture in Japan.  

7. Delete the shell script file
    ```shell
    rm -rf uncompressOldZipFiles.sh
    ```
8. Move back to the parent directory
    ```shell
    cd ..
    ```
### 5.2.3.  Inserting the old hourly data into the database.
1. Open the Python file 'insertOldHourlyObservationsData.py'
    ```shell
    vi insertOldHourlyObservationsData.py
    ```
2. Go to the following line:
    ```python
    conn = psycopg2.connect(database="", user="", password="", host="", port=5432)
    ```
3. Specify the appropriate database, user, password, host ipaddress of postgres, and port number.
    ```python
    conn = psycopg2.connect(database="soramame", user="aeros", password="aeros123", host="163.143.165.136", port=5432)
    ```
4. Save the file and exit.

9. Run the Python program 'insertNewHourlyObservationsData.py' by specifying the folder.
    ```shell
    python3 insertOldHourlyObservationsData.py ./temp
    ```

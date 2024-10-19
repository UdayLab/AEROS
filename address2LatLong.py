import googlemaps
import csv
import sys

def address2LatLong(inputfile,outputfile,client_key):
    """
    Generates point Information (latitude, longitude) for the given address and stores in the output csv file.
    
    input  : CSV File containing station Information (- stationInfo.csv in Data Folder)
    output : CSV File containing point Information (- stationAdd.txt in Data Folder)
    

    """
    
    iFilepath = inputfile
    oFilepath = outputfile
    line_count= 0

    # initialization of google maps function
    gmaps = googlemaps.Client(key=client_key)
    writeFile = open(oFilepath,'w+')
    csv_file = open(iFilepath, encoding="utf-8", errors="", newline="")
    inputFile = csv.reader(csv_file, delimiter=",")
    for line in inputFile:

        address = line[2]
        location  = gmaps.geocode(address)
        latitude = location[0]['geometry']['location'] ['lat']
        longitude=location[0]['geometry']['location']['lng']
        point ="Point("+str(longitude)+" "+str(latitude)+")"
        result =line[0] + ","+line[1] + ","+line[2] + ","+ str(point) + "\n"
        print(result)
        writeFile.write(result)
    writeFile.close()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Error : Incorrect number of input parameters given : "+ str(len(sys.argv) - 1))
        print("Input Parameters-> input FilePath, output Filepath, client key")
    else:
        address2LatLong(sys.argv[1], sys.argv[2], sys.argv[3])


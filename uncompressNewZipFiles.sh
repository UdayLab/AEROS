zipFiles=`ls *.zip`
for eachZipFile in $zipFiles
do
   unzip $eachZipFile
   rm $eachZipFile
done
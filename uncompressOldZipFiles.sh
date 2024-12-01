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
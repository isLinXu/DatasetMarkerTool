#！/bin/bash
let i=1
path=./
cd ${path}
for file in *.json
do
     labelme_json_to_dataset ${file}
     let i=i+1
done

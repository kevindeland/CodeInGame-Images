#!/bin/bash
for number in '01' '02' '03' '04' '05' '06' '07' '08' '09' '00' '11' '12' '13' '14' '15' '16' '17' '18' '19' '20'
do
   python3 src/color/kmeans.py -i ~/Downloads/axies/axie-$number.png -c 3 -o axie-output/axie-$number.png
done
exit 0

#!/bin/bash

for where in "Alabama" "Alaska" "Arizona" "Arkansas" "California" "Colorado" "Connecticut" "Delaware" "Florida" "Georgia" "Hawaii" "Idaho" "Illinois" "Indiana" "Iowa" "Kansas" "Kentucky" "Louisiana" "Maine" "Maryland" "Massachusetts" "Michigan" "Minnesota" "Mississippi" "Missouri" "Montana" "Nebraska" "Nevada" "New Hampshire" "New Jersey" "New Mexico" "New York" "North Carolina" "North Dakota" "Ohio" "Oklahoma" "Oregon" "Pennsylvania" "Rhode Island" "South Carolina" "South Dakota" "Tennessee" "Texas" "Utah" "Vermont" "Virginia" "Washington" "West Virginia" "Wisconsin" "Wyoming"  "DC" 
do
    for keyword in "data science scientist" 
    do
        echo $keyword > paramfile
        echo $where >> paramfile

        x=`echo $keyword | tr -d ' '`
        y=`echo $where | tr -d ' '`
        echo "scrapy crawl indeed_jobsearch > items.$x.$y.txt"
        echo killall chromedriver chromium
        scrapy crawl indeed_jobsearch > items.$x.$y.txt
        killall chromedriver chromium
        sleep 90
    done
done

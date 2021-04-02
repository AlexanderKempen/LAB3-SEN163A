For ZIP-File named: Lab 3 - Group 11

--- STEP 0: Importing packages ------------------------------------------------------------------------------------------------
The following packages and modules are used:
- requests
- pandas
- time
- numpy
- bs4 and BeautifulSoup
- concurrent.futures
- seaboard
- matplotlib.pyplot

--- STEP 1: Opening the zip ------------------------------------------------------------------------------------------------
When opening Lab 3 - Group 11.zip the following will be visible:
- README.txt
- scraping.py
- resultScraping.py
- analysis.py
- SEN163_Lab3_Group1.pdf
- Structure site.pptx

And two folders
- Graphs
- ResultsCSV

--- STEP 2: Handling the folder ------------------------------------------------------------------------------------------------
The textual assignment is can be accessed by opening: SEN163_Lab3_Group11.pdf
The scraping code can be accessed and run by opening: scraping.py
The analysis code can be accessed and run by opening: analysis.py

--- STEP 3: Running scraping.py ------------------------------------------------------------------------------------------------
Prerequisites:
Packages and modules

Use the scraping.py file for the web-scraping procedure on the https://news.tabularazor.org/ website.
This allows for retrieving all date used within the analysis, which should take a little over 1 hour.

Returns:
resultScraping.csv

--- STEP 4: Running analysis.py ------------------------------------------------------------------------------------------------
Prerequisites:
Packages and modules
resultScraping.csv

The analysis.py file is used for performing the anlaysis of the data retrieved from webscraping. When runn-
ing this file without having performed the webscraping first, it is important to have the resultScraping.csv
in the ResultCSV folder that is within the zip file as the the analysis.py calls upon this folder to retrieve
the csv script from. The Graphs resulting from the analysis are stored within the Graph folder that is also
already present within the Zip file.

This analysis produces several plots and dataframens and should take about 11 minutes to run.

Returns:
- Graphs
	AuthorPublicationPlot.png
	Boxplot.png
	Heatmap.png
	MaternityCheck.png

- ResultsCSV
	Couples over years.csv
	PublishingScheduleDays.csv

--- Step 5: The report ---------------------------------------------------------------------------------------------
The report contains all the textual and visual findings of the assignment.

All the best,

Team 11.

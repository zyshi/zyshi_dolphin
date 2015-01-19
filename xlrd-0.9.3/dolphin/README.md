Updates:
=========
- [Green] all the plots are now using d3 official templates
- [Green] all the visuals now can be generated automatically by visualization.py
- [Yellow] sort data file for line chart w/ xinput [TODO]

Visualization Process Done:
=========
- visualization.py is able to process the xls file to csv and tsv => [DONE]
- the scatter.html is able to plot the data in a rough way => [POLISH UP] => [DONE]
- visualization.py is able to generate the html file (string processor) [Scheduled on 1/14/15] => [DONE]
- polish up all the plots [Scheduled on 1/20/15] => [DONE]
- more type of plots will be provided [Scheduled on 1/15/15] => [DONE]

TODO:
=========
- check why pie chart only works with some coln [Scheduled on 1/19/15] 
- process incomplete data [Scheduled on 1/20/15]
- sort line chart data file by xinput [Scheduled on 1/19/15]

Build the Visualizaiton Project:
==========
- untar the xlrd package
- add the dolphin folder to the untarred folder
- install from the source in the folder ..../xlrd-0.9.3 install by type in cmd: $ python setup.py install  
- run the script visualization.py [set the plot_type = scatter], provide the x_index = 1980.0, y_index = 2009.0 as user inputs
- in the inner most dolphin folder run python -m SimpleHTTPServer 8000 &, you will be able to terminate the server by kill the processid
- open your browser @ http://localhost:8000/, select the file you want to view

Run the Visualization Project:
===========
- NOTE: the name of the coln must be exactly same as in the xls w/ blank spaces removed.
- scatter: use decimal xinput and yinput, the name of the coln must be exactly same as in the xls w/ blank spaces removed. e.g. x_index_name: 1980.0, y_index_name: 2009.0
- bar: use decimal yinput. e.g: x_index_name: Country, y_index_name: 2009.0
- pie: somehow some colns cannot be provide as value (need figure it out later).  e.g: group_index_name: Country, value_index_name: 2009.0
- line: decimal xinput and yinput. NOTE: the xinput currently must be automaitcally increnting (need figure it out later). e.g. x_index_name: Indent, y_index_name: 2009.0

FILES:
=========
- test1.xls: the same excel file 0Ah-EmCKc7VDydGljSHdfS1ZianFPQTZJTVpnZmNmV1E.xls
- visualization.py: currently processing the xls 3 csv, will add the html file generator tmr
- new_scatter_template.html: static hardcoded template
- line_template.html, bar_template.html, pie_template.html: template files
- d3: d3 files => [JS now retrieve the d3 files online]
Visualization Process Done:
=========
- visualization.py is able to process the xls file to csv
- the scatter.html is able to plot the data in a rough way
- visualization.py will be able to generate the html file (string processor) [Scheduled on 1/14/15] => [DONE]

TODO:
=========
- more type of plots will be provided [Scheduled on 1/15/15]
- polish up all the plots [Scheduled on 1/20/15]

Build the Visualizaiton Project:
==========
- untar the xlrd package
- add the dolphin folder to the untarred folder
- install from the source in the folder ..../xlrd-0.9.3 install by type in cmd: $ python setup.py install  
- run the script visualization.py [set the plot_type = scatter], provide the x_index = 1980.0, y_index = 2009.0 as user inputs
- in the inner most dolphin folder run python -m SimpleHTTPServer 8000 &, you will be able to terminate the server by kill the processid
- open your browser @ http://localhost:8000/scatter.html

FILES:
=========
- test1.xls: the same excel file 0Ah-EmCKc7VDydGljSHdfS1ZianFPQTZJTVpnZmNmV1E.xls
- visualization.py: currently processing the xls 3 csv, will add the html file generator tmr
- scatter_template.html: static hardcoded template, will polish up later
- d3: d3 files
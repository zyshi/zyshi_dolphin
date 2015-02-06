#!/bin/bash
ls -l
echo "Removing data files"
rm *.tsv
rm barplot_*.html*
rm scatterplot_*.html*
rm static/data*.tsv
ls -l
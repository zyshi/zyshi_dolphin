#!/bin/bash
echo "Removing auto visual plots htmls"
rm templates/auto_visual_*.html
echo "Removing supporting graph js files"
rm -r static/js/graph_js
echo "Removing supporting d3 data files"
rm -r static/data/*
echo "=== Clearing Finshed ==="
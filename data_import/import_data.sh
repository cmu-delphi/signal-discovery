#!/bin/sh


#!/bin/sh

BASE_URL="https://docs.google.com/spreadsheets/d/1zb7ItJzY5oq1n-2xtvnPBiJu2L3AqmCKubrLkKJZVHs/export?format=csv&gid="

wget "${BASE_URL}0" -O "data_sources.csv"
wget "${BASE_URL}1266808975" -O "signal_sets.csv"
wget "${BASE_URL}329338228" -O "signals.csv"
wget "${BASE_URL}214580132" -O "other_endpoint_data_sources.csv"
wget "${BASE_URL}1364181703" -O "other_endpoint_signals.csv"

#! Import Data Sources
python3 manage.py import datasources.resources.SourceSubdivisionResource --format=csv data_sources.csv --no-input
python3 manage.py import datasources.resources.SourceSubdivisionResource --format=csv other_endpoint_data_sources.csv --no-input
#! Import Signal Sets
python3 manage.py import signal_sets.resources.SignalSetResource --format=csv signal_sets.csv --no-input
#! Import Signals
python3 manage.py import signals.resources.SignalResource --format=csv signals.csv --no-input
python3 manage.py import signals.resources.SignalBaseResource --format=csv signals.csv --no-input
python3 manage.py import signals.resources.SignalResource --format=csv other_endpoint_signals.csv --no-input

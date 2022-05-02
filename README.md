# Audiosplit Package

A small project setting up the infrastructure for a neural network to be used for an audio demixer.

## Overview

Modern music is recorded in multiple stems and compressed into a final mix. Often amateur musicians use filtering and other methods to attempt to recreate the original stems.  

The objective is to create an AI that uses complex parameter filters to demix audio.  
  
This repository is the storage and display of the code used to prepare and use data for training audio demixers.  

### Overview of files in repository

* data
	* drums: 45 ten-second drum stems
	* guitar: 45 ten-second guitar stems
	* partdata.csv: compiled list of training data
* extra: extra images
* Main.ipynb: Explination and example of audiosplit.py
* audiosplit.py: Package  

### Data

The main data used for the example are 90 "stems" including 45 drum samples and 45 guitar samples. Found in "data/" in respective folders. Each loop is a 10 second ".wav" file. Drum and Guitar stems are mixed and matched to create "mixes" in the example (2025 total). Also included are precompiled predictions for the seperator as training data over part of the mixes.

The total size of the data folder combined is 144 MB.

### Software Setup
List all of the required packages:
* pydub
* matplotlib
* numpy
* pandas
* tensorflow

**Main.ipynb contains full walkthrough for implementation of the package**

#!/usr/local/bin/python
# -*- coding: utf-8 -*-

##############
### COLORS ###
##############

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;35m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1;34m'
BOLD=''
ORANGE='\033[1;31m'
NC='\033[0m'
NC=''



#####################################################
### B - SEARCH PHRASE IN FILES IN RANGE FROM - TO ###
#####################################################

phrase_seek_header = '|  SEEK FOR PHRASE WITHIN THE FILE  |  FILE NAME  |  '



##################################
### C - SEARCH BETWEEN PHRASES ###
##################################

phrase_between_header = '|  FILE FULL PATH  |  '
phrase_between_formatting_one_line = '%7i: %s'
phrase_between_formatting_begin_end = '###  %7i: %40s  ###'



#####################################
### D -PRINT FILES FROM TIMESTAMP ###
#####################################

input_date_pattern = r'\d\d:\d\d:\d\d\-\d\d\/\d\d\/\d\d\d\d'
datetime_pattern = '%H:%M:%S-%d/%m/%Y'
datetime_to_string_output = '%H:%M:%S   %d/%m/%Y'
files_output_header = '|    HOUR        DATE     |  FILE NAME  |  '
files_output_format = '|  %21s  |  %s'



##############################
### E -PRINT FILES BY SIZE ###
##############################

sort_size_header = '|     SIZE    |  FILE FULL PATH + NAME  |  '
sort_size_format = '|  %9s  |  %s'



############################################################################
### F - PRINT FILES BY SIZE RANGE -  UNIT SIZE FORMATTING / REFORMATTING ###
############################################################################

size_units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
unit_next_size = 1024
unit_next_size_float = 1024.0
unit_size_format = '%3.1f %s'
unit_size_last_format = '%.1f %s'

subhelp_for_size_range_pattern = 'python seeker.py -f bU-eU path'
subhelp_for_size_range_examples = [
									'python seeker.py -f "3KB-1MB D:\\Movies"',
									'python seeker.py -f "1-10GB /home/user_name/documents"',
									'python seeker.py -f "125KB-300KB C:\\Users\\Tomasz\\Desktop"',
									'python seeker.py -f "500MG-GB /tmp/"'
									]



##############################
### G -PRINT FILES BY SIZE ###
##############################

emtpy_files_header = '|  EMPTY FILES  |  '

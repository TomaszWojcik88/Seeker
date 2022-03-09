#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from os import path as os_path, listdir as os_listdir, walk as os_walk, stat as os_stat, getcwd as os_getcwd
from socket import gethostname as socket_gethostname
from sys import path as sys_path, exit as sys_exit, argv as sys_argv
from datetime import datetime
import argparse
# INTERNAL LIBRARIES #
import config, text, signs
GREEN, BLUE, RED, YELLOW, CYAN, NC, BOLD, ORANGE = config.GREEN, config.BLUE, config.RED, config.YELLOW, config.CYAN, config.NC, config.BOLD, config.ORANGE



class Seeker(object):

	#############################################################
	### ADDITIONAL FUNCTIONS FOR BELOW SCRIPT FUNCTIONALITIES ###
	#############################################################

	def menu(self, paths_to_interfaces_current_hostname):
		# LIMIT #
		if config.do_limit_to_one_choosen_interface_by_hostname[ socket_gethostname() ]:
			menu = ''.join([ signs.sign_newline, text.text_11, signs.sign_newline ])
			for counter, interface_full in enumerate(paths_to_interfaces_current_hostname):
				interface_name, path_to_messages = interface_full
				menu += ''.join([ str(counter + 1), signs.sign_dot_space, interface_name, signs.sign_newline ])
			print(menu)
			choice = int(input( text.text_12 ))
			return [ paths_to_interfaces_current_hostname[ (choice - 1) ] ]
		# DO NOT LIMIT #
		else:
			return paths_to_interfaces_current_hostname

	@staticmethod
	def header_and_footer(header_name, path_to_cwd):
		header_full = ''.join([ header_name, path_to_cwd, signs.sign_space, signs.sign_space, signs.sign_pipe ])
		header = ''.join([ signs.sign_star*len(header_full), signs.sign_newline, header_full,
							signs.sign_newline, signs.sign_star*len(header_full), signs.sign_newline ])
		footer = ''.join([ signs.sign_star*len(header_full), signs.sign_newline, ])
		return header, footer

	def load_files_list(self, path):
		if not os_path.exists(path):
			sys_exit(''.join([signs.sign_newline, text.text_20,
																path, text.text_23, signs.sign_newline]))
		if self.recursive:
			files_list = list()
			for root, dirs, files in os_walk(path, topdown=False):
				for file in files:
					file_full_path = os_path.join(root, file)
					files_list.append(file_full_path)
			return files_list
		else:
			return [ os_path.join(path, f) for f in os_listdir( path ) if os_path.isfile(os_path.join(path, f))]



	#################################
	### SEARCH FOR PHRASE IN LOGS ###
	#################################

	def subheader_and_subfooter(self, footer):
		footer_len = len(footer)
		digit_len = len(str(self.found_phrases_in_file ))
		footer_part_len = int((footer_len / 2) - (digit_len + 3))
		return ''.join([ signs.sign_hash*footer_part_len, signs.sign_space*3, str(self.found_phrases_in_file), signs.sign_space*4, signs.sign_hash*footer_part_len ])


	def search_for_phrase(self, file_list, start_index, full_log_path, phrase, footer ):
		for counter in range(start_index, len(file_list), 1):
			if phrase in file_list[counter]:
				self.found_phrases_in_file += 1
				header = self.subheader_and_subfooter(footer)
				self.file_output += ''.join([ header, signs.sign_newline ])
				limmited_list = file_list[counter-self.begin_range:counter+self.end_range]
				for line in limmited_list:
					if phrase in line:
						self.file_output += ''.join([ signs.sign_hash*5, signs.sign_space*5, line, signs.sign_space*5, signs.sign_hash*5, signs.sign_newline ])
					else:
						self.file_output += ''.join([ line, signs.sign_newline ])
				self.search_for_phrase(file_list, (counter+self.end_range), full_log_path, phrase, footer )
				break



	###################################################
	### PRINT CONTENT BEFORE AND AFTER FOUND PHRASE ###
	###################################################

	def search_phrase_plus_between_and_after_lines(self, arguments):
		# PHRASE #
		argument_array = arguments.split('---')
		if len(argument_array) != 3:
			sys_exit(''.join([signs.sign_newline, text.text_01, signs.sign_newline]))
		phrase = argument_array[0]
		if not ':' in argument_array[1]:
			sys_exit(''.join([signs.sign_newline, text.text_01, signs.sign_newline]))
		try:
			begin, end = argument_array[1].split(':')
			self.begin_range, self.end_range = int(begin), int(end)+1
		except:
			sys_exit(''.join([signs.sign_newline, text.text_01, signs.sign_newline]))
		# HOW MANY FILES TO CHECK #
		# FILES LIST #
		list_of_files = self.load_files_list(argument_array[2])
		list_of_files.sort(key=lambda file: os_path.getmtime(file), reverse=True)
		output = ''
		for file_in_list in list_of_files:
			file_output = ''
			try:
				header, footer = Seeker.header_and_footer(config.phrase_seek_header, argument_array[2])
				self.file_output = ''
				self.found_phrases_in_file = 0
				file_content = list()
				with open( file_in_list, 'r' ) as open_file:
					for line in open_file:
						file_content.append(line.strip('\n'))
				self.search_for_phrase(file_content, 0, file_in_list, phrase, footer)
				if len(self.file_output) != 0:
					output += ''.join([ header, self.file_output, footer ])
			except UnicodeDecodeError:
				continue
		if not output:
			header, footer = Seeker.header_and_footer(config.files_output_header, argument_array[2])
			output = ''.join([header, text.text_02, footer])
		print(output)



	#########################################
	### PRINT CONTENT BETWEEN TWO PHRASES ###
	#########################################

	def search_phrase_between_two_phrases(self, arguments):
		# CHECK ADDITIONAL ARGUMENTS #
		arguments_array = arguments.split('---')
		if len(arguments_array) != 3:
			sys_exit(text.text_11)
		begin_phrase, end_phrase = arguments_array[0], arguments_array[1]
		if not os_path.isfile(arguments_array[2]):
			sys_exit(''.join([signs.sign_newline, text.text_12, signs.sign_newline, arguments_array[2], signs.sign_newline]))
		# else:
		# 	list_of_files = self.load_files_list(arguments_array[2])
		# 	list_of_files.sort(key=lambda file: os_path.getmtime(file), reverse=True)
		output = ''
		try:
			file_content = list()
			file_output = ''
			with open(arguments_array[2], 'r') as open_file:
				file_content = open_file.readlines()
			do_add_line = False
			if_end_found = False
			for counter, line in enumerate(file_content):
				if end_phrase in line:
					do_add_line = False
					end_line = str( config.phrase_between_formatting_begin_end % ( counter, line.rstrip('\n'),  ),  )
					file_output += ''.join([ end_line, signs.sign_newline, signs.sign_hash*len(end_line), signs.sign_newline ])
					if_end_found = True
				if do_add_line:
					file_output += ( config.phrase_between_formatting_one_line % ( counter, line ) )
				if begin_phrase in line:
					do_add_line = True
					begin_line = (config.phrase_between_formatting_begin_end % (counter, line.rstrip('\n')))
					file_output += ''.join([ signs.sign_hash * len(begin_line), signs.sign_newline, begin_line, signs.sign_newline ])
			if not if_end_found:
				file_output = ''
			if len(file_output) > 0:
				header, footer = Seeker.header_and_footer(config.phrase_between_header, arguments_array[2])
				output += ''.join([ header, file_output, footer ])
			else:
				header, footer = Seeker.header_and_footer(config.phrase_between_header, arguments_array[2])
				output += ''.join([header, text.text_15, signs.sign_newline, footer])
		except UnicodeDecodeError:
			sys_exit(''.join([signs.sign_newline, text.text_16, signs.sign_newline]))
		print(output)



	########################################
	### PRINT FILES FROM GIVEN TIMESTAMP ###
	########################################

	def print_files_from_timestamp(self, argument, time):
		import re
		# CHECK BEGIN / END DATE #
		argument_list = argument.split( )
		for add_argument in argument_list[:2]:
			match = re.match(config.input_date_pattern, add_argument)
			if not match:
				sys_exit(text.text_18)
		# PARSE BEGIN AND END INPUT TO DATETIME #
		begin_date = datetime.strptime(argument_list[0], config.datetime_pattern)
		end_date = datetime.strptime(argument_list[1], config.datetime_pattern)
		if len(argument_list) > 2:
			path = argument_list[2]
		else:
			sys_exit(''.join([signs.sign_newline, text.text_17, signs.sign_newline]))
		# PREPARE LIST WITH FILE THAT FIT IN INTO THE TIMESTAMP #
		list_of_all_files_in_cwd = self.load_files_list(path)
		list_from_timestamp = list()
		if time=='last_modification':
			list_of_all_files_in_cwd.sort( key = lambda file: os_path.getmtime( os_path.join( path, file ) ), reverse=True )
			for file in list_of_all_files_in_cwd:
				file_last_modification_date = datetime.fromtimestamp( os_stat( os_path.join( path, file ) ).st_mtime )
				if file_last_modification_date > begin_date and file_last_modification_date < end_date:
					list_from_timestamp.append( [ file_last_modification_date, file ] )
				elif file_last_modification_date > end_date:
					break
		if time=='creation':
			list_of_all_files_in_cwd.sort( key = lambda file: os_path.getctime( os_path.join( path, file ) ), reverse=True )
			for file in list_of_all_files_in_cwd:
				file_creation_date = datetime.fromtimestamp( os_stat( os_path.join( path, file ) ).st_ctime )
				if file_creation_date > begin_date and file_creation_date < end_date:
					list_from_timestamp.append( [ file_creation_date, file ] )
				elif file_creation_date > end_date:
					break
		# IF LIST IS EMPTY THEN BREAK #
		if len(list_from_timestamp) == 0:
			sys_exit(''.join([ signs.sign_newline, text.text_19, signs.sign_newline ]) )
		# IF LIST IS NOT EMPTY THEN PRINT LIST #
		output = ''
		for line in list_from_timestamp:
			output += ''.join([ ( config.files_output_format % ( line[0].strftime(config.datetime_to_string_output),
																line[1]) ), signs.sign_newline ])
		header, footer = Seeker.header_and_footer(config.files_output_header, path)
		output = ''.join([ header, output, footer ])
		print(output)



	######################################
	### FUNCTIONS RELATED TO FILE SIZE ###
	######################################

	@staticmethod
	def format_size(size):
		for unit in config.size_units:
			if abs(size) > config.unit_next_size_float:
				size /= config.unit_next_size_float
			else:
				return config.unit_size_format % (size, unit)
		else:
			return config.unit_size_last_format % (size, config.size_units[-1])

	def format_size_to_digit(self, math_pow, size_unit):
		if size_unit.isdigit():
			return int(size_unit)
		size, unit = '', ''
		for letter in size_unit:
			if letter.isdigit(): size += letter
			else: unit += letter
		if not size: size = 1
		else: size = int(size)
		for counter, known_unit in enumerate(config.size_units):
			if unit == known_unit:
				unit_reformatted = math_pow(config.unit_next_size, counter)
				if unit_reformatted == 0: unit_reformatted += 1
				return int(size * unit_reformatted)
			elif unit == known_unit and counter == 0:
				return int(size)
		else:
			return unit



	### PRINT ALL FILES SORTED BY SIZE ###
	def print_all_files_sorted_by_size(self, path):
		files_list = self.load_files_list(path)
		files_list.sort(key=lambda file: os_path.getsize(file), reverse=True)
		output = ''
		output_files_list = ''
		for file in files_list:
			output_files_list += ''.join([config.sort_size_format % (Seeker.format_size(os_path.getsize(file)), file),
											signs.sign_newline])
		if len(output_files_list) == 0:
			output = ''.join([text.text_20, path, text.text_21])
		else:
			header, footer = Seeker.header_and_footer(config.sort_size_header, path)
			output = ''.join([header, output_files_list, footer])
		print(output)


	### PRINT ALL FILES FROM GIVEN SIZE RANGE ###
	def print_all_empty_files(self, argument):
		files_list = self.load_files_list(argument)
		files_list_zero = list()
		for file in files_list:
			if os_path.getsize(file) == 0:
				files_list_zero.append(file)
		if len(files_list_zero) == 0:
			sys_exit(''.join([signs.sign_newline, text.text_22, argument, signs.sign_newline]))
		output = ''
		for file in files_list_zero:
			output += ''.join([ file, signs.sign_newline ])
		header, footer = Seeker.header_and_footer(config.emtpy_files_header, argument)
		output = ''.join([header, output, footer])
		print(output)



	### PRINT ALL FILES FROM GIVEN SIZE RANGE ###
	def print_all_files_from_size_range(self, argument):
		# FORMAT ENTERED SIZE DATE - BASIC #
		from math import pow as math_pow
		argument_array = argument.split( )
		if os_path.isdir(argument_array[0]):
			statement = self.format_subhelp_for_size_range(text.text_33)
			sys_exit(statement)
		size_units_array = argument_array[0].split(signs.sign_minus)
		if len(size_units_array) < 2:
			statement = self.format_subhelp_for_size_range(text.text_10)
			sys_exit(statement)
		if not size_units_array[0] or not size_units_array[1]:
			statement = self.format_subhelp_for_size_range(text.text_10)
			sys_exit(statement)
		# FORMAT ENTERED SIZE #
		from_size = self.format_size_to_digit(math_pow, size_units_array[0])
		to_size = self.format_size_to_digit(math_pow, size_units_array[1])
		# CHECK ENTERED SIZE - ADVANCED #
		if not str(from_size).isdigit():
			statement = self.format_subhelp_for_size_range(''.join([ text.text_34, from_size]))
			sys_exit(statement)
		if not str(to_size).isdigit():
			statement = self.format_subhelp_for_size_range(''.join([ text.text_34, to_size]))
			sys_exit(statement)
		if from_size > to_size:
			statement = self.format_subhelp_for_size_range(text.text_35)
			sys_exit(statement)
		# LIST DIRECTORY FILES  #
		if len(argument_array) < 2:
			sys_exit(''.join([signs.sign_newline, text.text_09, signs.sign_newline]))
		else:
			path = argument_array[1]
		files_list = self.load_files_list(path)
		files_list.sort(key=lambda file: os_path.getsize(file))
		output = ''
		for file in files_list:
			file_size = os_path.getsize(file)
			if file_size > from_size and file_size < to_size:
				output += ''.join([config.sort_size_format % (Seeker.format_size(os_path.getsize(file)), file),
									signs.sign_newline])
				continue
			if file_size > to_size:
				break
		if len(output) == 0:
			output = ''.join([ signs.sign_newline, text.text_07, argument_array[0], signs.sign_newline ])
		else:
			header, footer = Seeker.header_and_footer(config.sort_size_header, path)
			output = ''.join([header, output, footer])
		print(output)

	def format_subhelp_for_size_range(self, error):
		examples = signs.sign_newline.join(config.subhelp_for_size_range_examples)
		current_units = ' | '.join(config.size_units)
		return signs.sign_newline.join([ '', error, '', text.text_24, config.subhelp_for_size_range_pattern,
							text.text_25, text.text_26,	text.text_27,text.text_28, examples,
							text.text_29, text.text_30, text.text_31, text.text_32, text.text_36, current_units ])





	############
	### INIT ###
	############

	def __init__(self, arguments):
		self.recursive=False
		if arguments.recursively:
			self.recursive=True
		if arguments.nu_before_nu_after:
			self.search_phrase_plus_between_and_after_lines(arguments.nu_before_nu_after)
		if arguments.between_two_phrases:
			self.search_phrase_between_two_phrases(arguments.between_two_phrases)
		if arguments.timestamp_last_modifycation:
			self.print_files_from_timestamp(arguments.timestamp_last_modifycation, time='last_modification')
		if arguments.timestamp_creation:
			self.print_files_from_timestamp(arguments.timestamp_creation, time='creation')
		if arguments.files_size_descending_path_to_folder:
			self.print_all_files_sorted_by_size(arguments.files_size_descending_path_to_folder)
		if arguments.files_size_from_given_range_ascending:
			self.print_all_files_from_size_range(arguments.files_size_from_given_range_ascending)
		if arguments.files_empty:
			self.print_all_empty_files(arguments.files_empty)





#####################
### LOAD FUNCTION ###
#####################

def load_arguments():
	try:
		parser = argparse.ArgumentParser(prog='Seeker', description='Application for checking and monitoring of indicated processes')
		parser.add_argument('-a', '--recursively', help='for any function will search recursively', default=False, action='store_true')
		parser.add_argument('-b', '--nu_before_nu_after', help='search phrase - in files. Print n line before and after phrase\nPattern: -b "PHRASE---nBP:bAP---/path/to/location"', default=None, type=str)
		parser.add_argument('-c', '--between_two_phrases', help='search phrase - all between 2 phrases. Pattern: -c "PHRASE_1---PHRASE_2---/path/to_file/file_name"', default=None, type=str)
		parser.add_argument('-d', '--timestamp_last_modifycation', help='timestamp\nPattern: -d "HH:MM:SS-DD/MM/YYYY HH:MM:SS-DD/MM/YYYY /path/to/location/"', default=None, type=str)
		parser.add_argument('-e', '--timestamp_creation', help='timestamp\nPattern: -e "HH:MM:SS-DD/MM/YYYY HH:MM:SS-DD/MM/YYYY /path/to/location/"', default=None, type=str)
		parser.add_argument('-f', '--files_size_descending_path_to_folder', help='print files by size - sorted descending. Example: -f /path/to/location/', default=None, type=str)
		parser.add_argument('-g', '--files_size_from_given_range_ascending', help='print files by size - from range bU-eU\nExample: -g "1KB-1MB /path/to/location/"', default=None, type=str)
		parser.add_argument('-i', '--files_empty', help='print files by size - empty\nExample: -f /path/to/location/', default=None, type=str)
		arguments = parser.parse_args()
		Seeker(arguments)
	except KeyboardInterrupt:
		sys_exit( menu_signs.sign_empty.join([ menu_signs.sign_newline_double, menu_text.error_keyboard_interrupt, menu_signs.sign_newline_double ]) )
	except IndexError as error:
		sys_exit( menu_signs.sign_empty.join([ menu_signs.sign_newline, menu_text.error_index_error, menu_signs.sign_newline_double, str(error), menu_signs.sign_newline_double ]))
	### HASH BELOW 2 LINES IF YOU WANT TO SEE MORE DETAILED INFO ABOUT ERRORS ###
	#except Exception as error:
	#	sys_exit(menu_signs.sign_empty.join([ menu_signs.sign_newline, menu_text.error_other_type_of_error, menu_signs.sign_newline_double, str(error), menu_signs.sign_newline_double ]))




if __name__ == "__main__":
	load_arguments()

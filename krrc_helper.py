
# code by Joe Meyer

# to use:
# 	load this file ("python -i krrc_helper.py") from Terminal/shell
#		make sure you're in same directory as playlist file (i.e. Downloads) AND this file (move it if necessary)
# 	call "normalize(filename, start_time, cumulative_time)"
#		- filename includes extension ('.txt' recommended) and refers to playlist/tracklist file
# 		- start_time is tuple(hours, minutes) [24 hour time] (see example below)
#		- cumulative_time indicates playlist time (if True) or individual song lengths (if False)
#			boolean
#			False by default
# 		ex: "normalize(file_name = 'playlist.txt', start_time = (15, 25), cumulative_time = True)"
# 			this creates new file 'playlist_normalized.txt' with normalized times
#			in this example start time is 15:25 [3:25 pm] and song times refer to location in playlist, not individual song lengths

# input file: file of format:
# 	"artist - song - time"
# 	new line separating each song
# 	ex: "AIR - Lucky and Unhappy - 00:00
# 		 Depeche Mode - People are People - 4:31
#		 Daft Punk - Technologic - 08:24" [cumulative_time]
#	  OR
#		"AIR - Lucky and Unhappy - 04:31
# 		 Depeche Mode - People are People - 3:53
#		 Daft Punk - Technologic - 4:44" [not cumulative_time]
#	IMPORTANT: lines must be exactly correct format
#		space or tab or dash followed directly by time followed directly by line break
#			time format: "[minutes]:[seconds]" (see example above)
#	'.doc' may not work; I recommend '.txt' extension for input file

# output: writes new file "[filename]_normalized.[extension]"
# 	same format, but times normalized to cumulative format from start time
#		24 hour time


class Normalizer:

	def __init__(self, old_file_name, start_time, cumulative_time = False):
		self.start_time = start_time
		self.cumulative_time = cumulative_time
		self.normalize_file(old_file_name)


	# creates new normalized file
	def normalize_file(self, old_file_name):
		new_file_name = self.new_file_name(old_file_name)
		# read from old file
		old_file = open(old_file_name, 'r')
		# create new file to write to
		new_file = open(new_file_name, 'w')
		# write to new file
		for old_line in old_file:
			song_info, song_time = self.parse_str(old_line)
			if (song_info and song_time and (':' in song_time)):
				# if time is successfully parsed from old_line, normalize time
				new_line = song_info + ' ' + self.normalize_time(song_time)
			else:
				# if no time parsed from old_line, copy old_line directly
				new_line = self.remove_linebreak(old_line)
			new_file.write(new_line+'\n')
		old_file.close()
		new_file.close()

	# appends "_normalized" to file name
	def new_file_name(self, file_name):
		raw_file_name, file_extension  = self.parse_str(file_name, separators = ['.'])
		self.check_parse(raw_file_name, file_extension)
		new_file_name = raw_file_name+"_normalized."+file_extension
		return new_file_name


	# splits string at last separator
	def parse_str(self, line, separators = [' ', '\t', '-']):
		index = -1
		while index >= - len(line):
			if line[index] in separators:
				return line[:index], line[index+1:]
			index -= 1
		print("failed to parse '{}'".format(self.remove_linebreak(line)))
		print("second part of str must have '{}' before it to parse".format(separators[0]))
		return None, None

	# raises exception if parse failed
	def check_parse(self, first_part, second_part):
		if not (first_part and second_part):
			raise Exception("parse failed")
		return first_part, second_part


	# adds self.start_time to time, returns song start time as string
	def normalize_time(self, time):

		# add start_time to time
		hours, minutes = self.offset_time(time)

		# save/update start time if necessary
		# not-cumulative_time indicates format is by song length (not cumulative playlist)
		if not self.cumulative_time:
			# new start_time for next song
			new_hours, new_minutes = hours, minutes
			# current song start time
			hours, minutes = self.simplify_time(self.start_time)
			# update start time for next song
			self.start_time = (new_hours, new_minutes)

		return self.format_time(int(hours), int(minutes))


	# takes time str, offsets by start_time, returns hours, min.s as floats
	def offset_time(self, time):
		# split time into minutes, seconds
		minutes, seconds = self.parse_str(time, ':')
		# check that split worked, throw error if not
		self.check_parse(minutes, seconds)
		# discard line break if necessary
		seconds = self.remove_linebreak(seconds)
		# convert from str to int
		minutes, seconds = int(minutes), int(seconds)

		# add offset
		hours = self.start_time[0]
		minutes += self.start_time[1] + seconds/60.

		# format to standard time
		hours, minutes = self.simplify_time((hours, minutes))

		return hours, minutes


	# converts time to str, returns it
	def format_time(self, hours, minutes):
		hours = self.normalize_time_str(str(hours))
		minutes = self.normalize_time_str(str(minutes))
		time_str = str(hours)+':'+str(minutes)
		return time_str


	# normalizes length of time str (prepends '0' if necessary)
	def normalize_time_str(self, time_str):
		if len(time_str)<2:
			time_str = '0'+time_str
		return time_str

	# format to standard time (return as floats)
	def simplify_time(self, (hours, minutes)):
		hours = (hours + (minutes//60.)) % 24.
		minutes = minutes%60.
		return hours, minutes

	def remove_linebreak(self, line):
		if line[-1] == '\n':
			return line[:-1]
		return line



# main function
def normalize(file_name, start_time, cumulative_time = False):
	Normalizer(file_name, start_time, cumulative_time)









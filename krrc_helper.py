
# code by Joe Meyer

# to use:
# 	load this file ("python -i krrc_helper.py")
#		make sure you're in same directory as playlist file (i.e. Desktop) AND this file (move it if necessary)
# 	call "normalize(filename, start_time, cumulative_time)"
#		- filename includes extension
# 		- time is tuple(hours, minutes)
#		- cumulative_time indicates playlist time (if True) or individual song lengths (if False)
#			boolean
#			False by default
# 		ex: "normalize(file_name = 'testfile.txt', start_time = (15, 25), cumulative_time = True)"
# 			this creates new file testfile_normalized.txt with normalized times
#			in this example start time is 15:25 and song times refer to location in playlist, not individual song lengths

# input file: file of format:
# 	"artist - song - time"
# 	new line separating each song
# 	ex: "AIR - Lucky and Unhappy - 00:00
# 		 Depeche Mode - People are People - 04:31
#		 Daft Punk - Technologic - 08:24" [cumulative_time]
#	  OR
#		"AIR - Lucky and Unhappy - 04:31
# 		 Depeche Mode - People are People - 3:53
#		 Daft Punk - Technologic - 4:44" [not cumulative_time]
#	IMPORTANT: lines must be exactly correct format
#		no spaces at end of lines
#		line break after every line
#		no pm or am indicator at end of lines
#		24 hour time
#			hours, minutes separated by ':'
# 	input start time : (hours, minutes) [24 hour time]

# output: writes new file "[filename]_normalized.[extension]"
# 	same format, but times normalized to cumulative format from start time


class Normalizer:

	def __init__(self, old_file_name, start_time, cumulative_time = True):
		self.start_time = start_time
		self.normalize_file(old_file_name, cumulative_time)


	def normalize_file(self, old_file_name, cumulative_time):
		new_file_name = self.new_file_name(old_file_name)
		# read from old file
		old_file = open(old_file_name, 'r')
		# create new file to write to
		new_file = open(new_file_name, 'w')
		# write to new file
		for old_line in old_file:
			song_info, song_time = self.parse_str(old_line)
			new_line = song_info+' '+self.normalize_time(song_time, cumulative_time)
			new_file.write(new_line+'\n')
		old_file.close()
		new_file.close()

	# appends "_normalized" to file name
	def new_file_name(self, file_name):
		raw_file_name, file_extension = self.parse_str(file_name, separator = '.')
		new_file_name = raw_file_name+"_normalized."+file_extension
		return new_file_name


	# splits string at last separator
	def parse_str(self, line, separator = ' '):
		index = -1
		while index >= - len(line):
			if line[index] is separator:
				return line[:index], line[index+1:]
			index -= 1
		raise Exception("time must have '{}' before it".format(separator))


	# adds self.start_time to time, returns song start time as string
	# cumulative_time indicates format (cumulative playlist vs individual song times)
	def normalize_time(self, time, cumulative_time):

		# add start_time to time
		hours, minutes = self.offset_time(time)

		# save/update start time if necessary
		if not cumulative_time:
			# new start_time for next song
			new_hours, new_minutes = hours, minutes
			# current song start time
			hours, minutes = self.start_time
			# update start time for next song
			self.start_time = (new_hours, new_minutes)

		return self.format_time(hours, minutes)


	# takes time str, offsets by start_time, returns hours, min.s as ints
	def offset_time(self, time):
		# split time into hours, minutes
		hours, minutes = self.parse_str(time, ':')
		# discard line break if necessary
		if minutes[-1] is '\n':
			minutes = minutes[:-1]
		# convert from str to int
		hours, minutes = int(hours), int(minutes)

		# add offset
		hours += self.start_time[0]
		minutes += self.start_time[1]

		# format to standard time
		hours += minutes//60
		hours = hours%24
		minutes = minutes%60

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



def normalize(file_name, start_time, cumulative_time = False):
	Normalizer(file_name, start_time, cumulative_time)









import threading
import numpy as np
import time
import serial


class ImageStream:
	def __init__(self, inputStream=input, outputStream=print, maxFPS=1200):
		# Store the location of the iput and output streams
		self._inputStream = inputStream
		self._outputStream = outputStream

		# Array to hold the buffered lines
		self._lines = []

		# Loopy stuff...
		self._isLooping = False
		self._fullLoopRead = False
		self._loopIndex = -1
		self._loopStart = -1

		# Variable to store whether the input stream has ended
		self._isStreamEnded = False

		# Set a default maximum frame rate
		self.maxFPS = maxFPS

		# Connected to the Arduino?
		self._isConnected = False
		self._serialConnection = None

	# Attempts to connect to the Arduino
	def connectToArduino(self):
		for i in range(100):
			try:
				self._serialConnection = serial.Serial('/dev/ttyACM' + str(i), 115200)
				print('Connected to ttyACM' + str(i))
				time.sleep(2)
				self._isConnected = True
			except:
				pass
		self._isConnected = False

	# Method to start the picture running through
	def begin(self):
		# Start a thread that continously reads in the line data
		self._readerThread = threading.Thread(target=self._read)
		self._readerThread.start()

		self._outputStream("CLEAR")

	# Method to print a line out to the output stream
	def printLine(self, line):
		self._outputStream(line)

	# Write lines to Arduino
	def displayLine(self, line):
		if self._isConnected:
			lineString = ""
			for val in line.data:
				lineString += chr(val[0]//2)
				lineString += chr(val[1]//2)
				lineString += chr(val[2]//2)
			print.write(lineString.encode('ascii'))

	# Method to get the next line from the buffer
	def getNextLine(self):
		# Keep things from going too fast
		if self.maxFPS > 0: time.sleep(1/self.maxFPS)

		# If we are not looping, just return the next line out of the array
		if not self._isLooping or self._loopStart != 0:

			# If there are no lines, return a solid black line
			if len(self._lines) == 0:
				return ImageLine()

			# If there is only one line, return itlineString += chr(val[0]).encode('ascii')
			elif len(self._lines) == 1:
				return self._lines[0].copy()

			# If there are more than one lines, return the first line and then
			# 	remove it from the array
			else:
				line = self._lines[0]
				self._lines = self._lines[1:]
				return line

		# If we are looping
		else:
			# Begin the loopiness

			# If we are'nt at the end of the loop yet
			if self._loopIndex < len(self._lines) - 1:
				# Continue on through the loop
				self._loopIndex += 1
			# Go back to he beginning of the loop ONLY if the entire loop has been read
			elif self._fullLoopRead:
				self._loopIndex = 0

			# Now that we know where we are in the loop, we can return that line
			return self._lines[self._loopIndex].copy()

	# Method to check if all lines have been read, or if the reader is looping
	def isDone(self):
		return self._isStreamEnded and not self._isLooping

	# Method to stop the input stream from being read
	def stopReading(self):
		self._isStreamEnded = True

	# Method to stop everything...
	def kill_KILL(self):
		self._isStreamEnded = True
		self._isLooping = False

	# Method that will continously loop around, reading data from the input stream
	# Note that because this is basically an infinte loop, it should only be started in a thread
	def _read(self):
		# While we still have data to read and haven't been told to stop
		while not self._isStreamEnded:
			try:
				# Read the line
				line = self._inputStream()

				# If the command was to clear, immediataly flush all input
				if line == "CLEAR":
					lines = []

				# Command to start a loop
				elif line == "LOOP":
					# Start loopiness
					self._isLooping = True
					self._fullLoopRead = False
					self._loopStart = len(self._lines)
					self._loopIndex = 0

				# TODO: read in ALOOP stuff...

				#If the loop is to be ended
				elif line == "ENDLOOP":
					#End loopiness...
					self._fullLoopRead = True

				# Else, we should just be boring and stick the line onto the end of the list
				else: self._lines.append(ImageLine(line))

			# If something bad happened...
			except EOFError:
				# Stop reading stuff
				self._isStreamEnded = True


class ImageLine:
	def __init__(self, data=""):

		# Make sure that the data is the right length
		if len(data) > 1800:
			data = data[0:1800]

		# Create a numpy array to hold the data
		# TODO: determine whether it will be more efficient to use numpy or just normal arrays
		self.data = np.zeros((300,3), dtype=np.uint8)

		#print(self.data)
		#Step over every two bit part of the input
		for i in range(0,len(data),6):
			self.data[i//6,0] = int(data[i:i+2], 16)
			self.data[i//6,1] = int(data[i+2:i+4], 16)
			self.data[i//6,2] = int(data[i+4:i+6], 16)

	def __str__(self):
		string = ""
		for i in self.data:
			string += "%02X" % i[0]
			string += "%02X" % i[1]
			string += "%02X" % i[2]
		return string

	def copy(self):
		other = ImageLine()
		other.data = self.data.copy()
		return other

	def getColorAt(self, index):
		if index >= 0 and index < 300:
			return Color(self.data[index][0], self.data[index][1], self.data[index][2])

	def setColorAt(self, index, color):
		if index >= 0 and index < 300:
			self.data[index][0] = color.r
			self.data[index][1] = color.g
			self.data[index][2] = color.b

class Color:
	def __init__(self, r=0, g=0, b=0):
		self.r = r
		self.b = b
		self.g = g

	# TODO: add fun filter-y stuff here

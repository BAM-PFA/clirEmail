class Email:
	"""docstring for ClassName"""
	def __init__(self,
				 name,
				 deceased,
				 titles,
				 dates,
				 recordIDs):
		
		self.name = name
		self.deceased = deceased
		self.titles = titles
		self.dates = dates

		self.PAR_1 = 'Dear [FULL NAME],\n\n'
		self.PAR_2 = '''The Berkeley Art Museum and Pacific Film Archive (BAMPFA) has received a grant from the Council on Library and Information Resources (CLIR) to digitize nearly 800 audio cassette tapes of guest speakers at the Pacific Film Archive, recorded between 1976 and 1986. As part of this project, we have digitized one or more audio recordings in which you were a participant.\n\n'''
		self.PAR_3 = '''The following recording date(s) represent your contributions to this collection that have been digitized:\n\n'''
		self.PAR_4 = '' # list of event dates
		self.PAR_5 = '\n\nThe following film titles were discussed in the relevant recordings:\n\n'
		self.PAR_6 = '' # List of film titles
		self.PAR_7 = '''\n\nAs part of the educational mission of this project, BAMPFA respectfully requests your permission to make these recordings available online via educational partners such as the Internet Archive and/or the BAMPFA website. This project also enables us to preserve these works for researchers into the future as digital formats change. Please note that speakers and/or their heirs retain copyright to their content unless they explicitly waive copyright.\n\n'''
		self.PAR_8 = '''Please complete this two-question Google form [URL] to record your response to our request.\n\n'''
		self.PAR_9 = '''Thank you for participating in this exciting project!\n\n\n'''
		self.PAR_10 = 'Sincerely,\n\n'
		self.PAR_11 = 'Michael Campos-Quinn and Jason Sanders\n'
		self.PAR_12 = 'BAMPFA Film Library and Study Center'

		self.allParagraphs = None
		self.reversedParagraphs = None

	def paragraphs_to_list(self):
		self.allParagraphs = [
			self.PAR_1,
			self.PAR_2,
			self.PAR_3,
			self.PAR_4,
			self.PAR_5,
			self.PAR_6,
			self.PAR_7,
			self.PAR_8,
			self.PAR_9,
			self.PAR_10,
			self.PAR_11,
			self.PAR_12
			]

	def reverse_paragraphs(self):
		self.reversedParagraphs = reversed(self.allParagraphs)

	def dear(self):
		self.PAR_1 = self.PAR_1.replace('[FULL NAME]',self.name)

	def is_deceased(self):
		if self.deceased == 'y':
			self.PAR_1 = "To the estate of {} ('THE ESTATE'):\n\n".format(self.name)
			self.PAR_2 = self.PAR_2.replace(
				'in which you were a participant.',
				'in which {} was a participant.'.format(self.name)
				)
			self.PAR_3 = self.PAR_3.replace(
				'your contributions',
				'the contributions of {}'.format(self.name)
				)
			self.PAR_7 = self.PAR_7.replace(
				'your permission',
				'the permission of THE ESTATE'
				)
		else:
			pass

	def test_dates(self):
		if self.dates in ('',[],['']):
			self.PAR_3 = self.PAR_4 = None
		else:
			self.PAR_4 = '\n'.join(self.dates)

	def test_titles(self):
		if self.titles in ('',[],['']):
			self.PAR_5 = self.PAR_6 = None
		else:
			self.PAR_6 = '\n'.join([title.upper() for title in self.titles])

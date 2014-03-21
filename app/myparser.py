from xml.dom import minidom
import os

allProjects = None
counter = 0
#stores an entire directory of SVN data
class svnStore:
	def __init__(self):
		self.dict = {}

	def storeFile(self, tempFile):
		if tempFile.projname not in self.dict:
			tempObj = projectObj()
			self.dict[tempFile.projname] = tempObj
		self.dict[tempFile.projname].addFile(tempFile)

	def storeLogEntry(self, tempEntry):
		if tempEntry.projname in self.dict:
			for i in self.dict[tempEntry.projname].list:
				for j in tempEntry.paths:
					if i.path == j:
						i.addLogToFile(tempEntry)
			if(self.dict[tempEntry.projname].commitMessage == None):
				self.dict[tempEntry.projname].commitMessage = tempEntry.message

	def getProject(self, name):
		return self.dict[name]
						
#Stores information about a project, including files and comments
class projectObj:
	def __init__(self):
		self.list = []
		self.title = None
		self.version = None
		self.date = None
		self.commitMessage = None
		self.pathdict = {}

	def addFile(self, tempFile):
		if(self.title is None):
			self.title = tempFile.projname
			self.version = tempFile.version
			self.date = tempFile.date
		self.list.append(tempFile)
		self.pathdict["/"+tempFile.author + "/" + tempFile.path] = tempFile

#stores file information
class fileObj:
	def __init__(self, xmlobj):
		global counter
		self.id = counter
		counter = counter + 1
		self.commits = []
		self.type = xmlobj.attributes["kind"].value
		self.path = xmlobj.getElementsByTagName('name')[0].firstChild.data
		if(self.type != "dir" and (self.path).rfind('.')>-1):
			self.type = self.path[self.path.rfind('.')+1:]

		self.url = "https://subversion.ews.illinois.edu/svn/sp14-cs242/lato2/" + self.path
		if(self.path.find("/")>-1):
			self.projname = self.path[0:self.path.find("/")]
		else:
			self.projname = self.path
		self.url = self.path.replace("/", "-")
		commit = xmlobj.getElementsByTagName('commit')[0]
		self.version = commit.attributes["revision"].value
		self.date = commit.getElementsByTagName('date')[0].firstChild.data[0:10]
		self.author = commit.getElementsByTagName('author')[0].firstChild.data
		if(self.type != "dir"):
			self.size = xmlobj.getElementsByTagName('size')[0].firstChild.data
		else:
			self.size = 0
		self.formattedInfo = "";

	def addLogToFile(self, tempObj):
		self.commits.append(tempObj)

#stores log information
class logObj:
	def __init__(self, xmlobj):
		self.projname = None
		self.paths = []
		self.version = xmlobj.attributes["revision"].value
		self.date = xmlobj.getElementsByTagName('date')[0].firstChild.data[0:10]
		self.author = xmlobj.getElementsByTagName('author')[0].firstChild.data[0:10]
		for i in xmlobj.getElementsByTagName('path'):
			self.paths.append(i.firstChild.data[(len(self.author)+2):])
			if(self.projname is None):
				tempstr = i.firstChild.data[(len(self.author)+2):]
				if(tempstr.find("/")>-1):
					self.projname = tempstr[0:tempstr.find("/")]
				else:
					self.projname = tempstr
		self.message = xmlobj.getElementsByTagName('msg')[0].firstChild.data
			
tempdir = os.getcwd()

#Generates commit messages for fileObjs after generation
def generateCommits(store):
	for i in store.dict:
		for currfile in store.dict[i].list:
			for commit in currfile.commits:
				currfile.formattedInfo += commit.version + " - " + commit.date + " - " + commit.author + commit.message + "**"
		print currfile.formattedInfo

#parses the svn log, returing an svnStore object
def parse():
	global allProjects
	if allProjects is None:
		os.chdir(tempdir +  "/app/static/data")
		allProjects = svnStore()

		listdoc = minidom.parse('svn_list.xml')
		entries = listdoc.getElementsByTagName("entry")
		for singleEntry in entries:
			tempobj = fileObj(singleEntry)
			allProjects.storeFile(tempobj)

		logdoc = minidom.parse('svn_log.xml')
		logEntries = logdoc.getElementsByTagName("logentry")
		for singleEntry in logEntries:
			tempentry = logObj(singleEntry)
			allProjects.storeLogEntry(tempentry)
		generateCommits(allProjects)
	return allProjects;
if  __name__ =='__main__':
	temp = parse()
	temp2 = temp.dict["HW0"]
	temp3 = temp2.list[0]
	print "proj", temp3.path

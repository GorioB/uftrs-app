import time,datetime,calendar
TZ_OFFSET=-8
def getEpochTime():
	return int(time.time())

def getStringTime():
	d = datetime.datetime.now()
	return '{:%Y-%m-%d %H:%M:%S}'.format(d)

def stringToSecs(s):
	s = s.replace(" ",":")
	s = s.replace("-",":")
	timeArray = map(int,s.split(":"))
	d = datetime.datetime(timeArray[0],timeArray[1],timeArray[2],timeArray[3],
		timeArray[4],timeArray[5])
	return calendar.timegm(d.timetuple())+(TZ_OFFSET*60*60)#hardcoded because hassle
	
def secsToString(s):
	return '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.fromtimestamp(float(s)))
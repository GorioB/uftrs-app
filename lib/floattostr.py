def floatToStr(f):
	return '{:20,.2f}'.format(f).strip()

def strToFloat(s):
	if s=="":
		return 0
	return float(s.replace(",",""))
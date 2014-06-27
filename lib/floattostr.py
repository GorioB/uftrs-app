def floatToStr(f):
	return '{:20,.2f}'.format(f).strip()

def strToFloat(s):
	return float(s.replace(",",""))
from lib.floattostr import *
def tab(n=1):
	return "    "*n
def floatToStrParenNeg(n):
	if n<0:
		return "("+floatToStr(n).strip("-")+")"
	else:
		return floatToStr(n)

def getNotePreviewLines(notes):
	notes = sorted(notes,key=lambda l:int(l.noteNumber.content))
	noteBlocks = [[note for note in notes if note.noteNumber.content==nn] for nn in sorted(set([i.noteNumber.content for i in notes]),key=lambda p:int(p))]
	
	noteBlocksSegregated = reduce(list.__add__,[segregateBlocks(block) for block in noteBlocks])
	return [generateBlockInfo(g) for g in noteBlocksSegregated]

def generateBlockInfo(block):
	if block[0].identifier=="COCPNote":
		lines=[]
		inflows = [i for i in block if i.flowDirection.content=="Inflow"]
		outflows = [i for i in block if i.flowDirection.content=="Outflow"]
		lines.append([[block[0].noteNumber.content+". "+block[0].event.content,"","","",""],
			[0,0,0,0,0],
			[1,0,0,0,0]])
		totalInflows=0
		totalOutflows=0
		if inflows:
			lines.append([["Inflows",'','','',''],
				[0,0,0,0,0],
				[0,0,0,0,0]])
			for inflow in inflows:
				nature=inflow.nature.content
				amount = inflow.amount.content
				try:
					amount=float(amount)
				except:
					amount=0
				lines.append([[tab(1)+nature,'',floatToStrParenNeg(amount),'',''],
					[0,0,0,0,0],
					[0,0,0,0,0]])
				totalInflows+=amount
			lines.append([[tab(2)+"Total Inflows",'','','',floatToStrParenNeg(totalInflows)],
				[0,0,0,0,0],
				[0,0,0,0,0]])
		if outflows:
			lines.append([["Outflows",'','','',''],
				[0,0,0,0,0],
				[0,0,0,0,0]])
			for outflow in outflows:
				nature=outflow.nature.content
				amount = outflow.amount.content
				try:
					amount=float(amount)
				except:
					amount=0
				lines.append([[tab(1)+nature,'',floatToStrParenNeg(amount),'',''],
					[0,0,0,0,0],
					[0,0,0,0,0]])
				totalOutflows+=amount
			lines.append([[tab(2)+"Total Outflows",'','','',"("+floatToStrParenNeg(totalOutflows)+")"],
				[0,0,0,0,0],
				[0,0,0,0,0]])
		lines.append([["Net Cash Flow",'','','P',floatToStrParenNeg(totalInflows-totalOutflows)],
			[0,0,0,0,2],
			[0,0,0,0,0]])
		return NoteBlock("table",lines)


	else:
		if block[0].identifier=="LTINote":
			lines=''
			for i in block:
				lines+=i.notes.content+'\n'

			return NoteBlock("text",[block[0].noteNumber.content+". "+"Long Term Investment",lines])
		if block[0].identifier=="OONote":
			for i in block:
				lines+=i.notes.content+'\n'

			return NoteBlock("text",[block[0].noteNumber.content+'. '+"Other Outflow",lines])
		if block[0].identifier=="ODNote":
			for i in block:
				lines+=i.notes.description+'\n'
			return NoteBlock("text",[block[0].noteNumber.content+". "+"Other Descritive Note",lines])

def segregateBlocks(block):
	return [[note for note in block if note.identifier==ident] for ident in set([i.identifier for i in block])]

class NoteBlock(object):
	def __init__(self,blockType,payload):
		self.blockType=blockType
		self.payload=payload
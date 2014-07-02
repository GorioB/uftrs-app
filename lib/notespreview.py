from Tkinter import *
from ttk import *
import lib.app
from lib.models import *

def gatherNotes(app):
	notes = {}
	COCPNotes = app._listGeneral(COCPNote,False)
	LTINotes = app._listGeneral(LTINote,False)
	OONotes = app._listGeneral(OONote,False)
	ODNotes = app._listGeneral(ODNote,False)

	cocpEvents = [i for i in COCPNotes]
	cocpEventsKeys = list(set([i.event.content for i in cocpEvents]))
	for event in cocpEventsKeys:
		notes[event]={u"Inflows":{},u"Outflows":{}}
		eventNotes = [i for i in cocpEvents if i.event.content==event]
		inflows = [i for i in eventNotes if i.flowDirection.content=="Inflow"]
		outflows = [i for i in eventNotes if i.flowDirection.content=="Outflow"]
		for inflow in inflows:
			if inflow.nature.content in notes[event].keys():
				notes[event][u'Inflows'][inflow.nature.content]+=int(inflow.amount.content)
			else:
				notes[event][u'Inflows'][inflow.nature.content]=int(inflow.amount.content)
		for outflow in outflows:
			if outflow.nature.content in notes[event].keys():
				notes[event][u'Outflows'][outflow.nature.content]+=int(outflow.amount.content)
			else:
				notes[event][u'Outflows'][outflow.nature.content]=int(outflow.amount.content)
	if LTINotes:
		notes[u'Long Term Investment']=[]
		for note in LTINotes:
			notes['Long Term Investment'].append(note.purpose.content)

	if OONotes:
		notes[u'Other Outflows']=[]
		for note in OONotes:
			notes['Other Outflows'].append(note.purpose.content)

	if ODNotes:
		notes[u'Other Descriptive Notes']=[]
		for note in ODNotes:
			notes['Other Descriptive Notes'].append(note.description.content)

	return notes

def numberNotes(notes):
	notesKeys = notes.keys()
	sortedNotes = sorted([i for i in notesKeys if i not in ("Long Term Investment","Other Outflows","Other Descriptive Notes")],
		key=lambda label:label[0])+[i for i in ("Long Term Investment","Other Outflows","Other Descriptive Notes") if i in notesKeys]
	return sortedNotes


if __name__=="__main__":
	app = lib.app.App()
	notes = gatherNotes(app)
	nn = numberNotes(notes)
	print nn
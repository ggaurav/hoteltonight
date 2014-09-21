from datetime import date
from sqlalchemy import Float

def normalize(row):
	def convert_datetime(value):
		return value.strftime("%Y-%m-%d %H:%M:%S")
	newRow = []	
	for elem in row:		
		if isinstance(elem, date):
			newRow.append(convert_datetime(elem))
			
		elif isinstance(elem, Float):
			newRow.append(float(elem))
		else:
			newRow.append(elem)	
	return tuple(newRow)

def _formatTo6Digits(inp):
	op = float(inp)*1000000
	op = str(op).replace('.','')[0:8]
	#op = str(op).replace('.','')
	return op	
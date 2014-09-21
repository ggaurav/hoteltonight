import json

class SuccessResp(): 
	def __init__(self,callback,data):
		res_dict = dict(status = 'success', data=data)
		self.res_json = json.dumps(res_dict)
		if callback:
			self.res_json = callback + "(" + self.res_json + ")"
	
	def __repr__(self):
		return self.res_json

class ErrorResp(): 
	def __init__(self,callback,data=[], err_msg = 'There is some error', err_code = 0):
		res_dict = dict(status = 'error', data = data, error_msg = err_msg, error_code = err_code)
		self.res_json = json.dumps(res_dict)
		if callback:
			self.res_json = callback + "(" + self.res_json + ")"
		
	def __repr__(self):
		return self.res_json
	
		
		
	

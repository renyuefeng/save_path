import re
import pandas as pd
import numpy as np
from pycorrector.macbert.macbert_corrector import MacBertCorrector

from .pdfMethod import clean_data, pd_output_str
import datetime

# 买卖数据信息抽取
class dealContractMessage:
	"""docstring for ClassName"""
	def __init__(self, main_str):
		self.strings = main_str
		# self.nlp = MacBertCorrector("shibing624/macbert4csc-base-chinese").macbert_correct
		# if isinstance(main_str, str):
		# 	self.df = pd.DataFrame({'main': [main_str]})
		# else:
		# 	self.strings = main_str

	# @pd_output_str
	def searchA(self):
		# patternB = re.compile('乙[(（\w)）]+?[:：]+?[ ]*?(\w+)|需方[(（\w)）]*?[:：]+?[ ]*?([()（）\w]+)')
		# self.df['first_party'] = list(map(lambda x: patternA.search(x).group() if pd.notna(x) and patternA.search(x) != None else np.nan, self.df[lis]))
		# self.df['second_party'] = list(map(lambda x: patternB.search(x).group() if pd.notna(x) and patternB.search(x) != None else np.nan, self.df[lis]))
		# self.df = clean_data(self.df, col='first_party', pattern_str='\w', method='search')
		# self.df = clean_data(self.df, col='second_party', pattern_str='\w', method='search')
		patternA = re.compile('甲[(（\w)）]+?[:：]+?[ ]*?([()（）\w ]+)|供方[(（\w)）]*?[:：]+?[ ]*?([()（）\w ]+)')
		try:
			strings = patternA.search(self.strings).group()
			strings = clean_data(strings, pattern_str='\w', method='search')
		except:
			strings = ''
		return strings

	def searchB(self):
		patternB = re.compile('乙[(（\w)）]+?[:：]+?[ ]*?([()（）\w]+)|需方[(（\w)）]*?[:：]+?[ ]*?([()（）\w]+)')
		try:
			strings = patternB.search(self.strings).group()
			strings = clean_data(strings, pattern_str='\w', method='search')
		except:
			strings = ''
		return strings

	def search_contract_number(self):
		pattern = re.compile('合同编号：(\w+)')
		try:
			strings = pattern.search(self.strings).group()
			strings = clean_data(strings, pattern_str='\w', method='search')
		except:
			strings = ''
		return strings

	# @pd_output_str
	# def searchAAndBPhone(self, lis='main'):
	#
	# 	pattern = re.compile('(?<=)[电话手机][\w ]+[:： ]*?[\d\- ]+')
	# 	self.df['APhone'] = list(map(lambda x: pattern.findall(x)[0] if pd.notna(x) and pattern.search(x)!=None else np.nan, self.df[lis]))
	# 	self.df['BPhone'] = list(map(lambda x: pattern.findall(x)[1] if pd.notna(x) and pattern.search(x)!=None else np.nan, self.df[lis]))
	#
	# 	self.df = clean_data(self.df, col='APhone', pattern_str='\d', method='sub')
	# 	self.df = clean_data(self.df, col='BPhone', pattern_str='\d', method='sub')
	#
	# 	return self.df

	def searchAPhone(self):
		pattern = re.compile('(?<=)[电话手机][\w ]+[:： ]*?[\d\- ]+')
		try:
			strings = pattern.findall(self.strings)[0]
			strings = clean_data(strings, pattern_str='\d', method='search')
		except:
			strings = ''
		return strings

	def searchBPhone(self):
		pattern = re.compile('(?<=)[电话手机][\w ]+[:： ]*?[\d\- ]+')
		try:
			strings = pattern.findall(self.strings)[1]
			strings = clean_data(strings, pattern_str='\d', method='search')
		except:
			strings = ''
		return strings

	def searchAPiece(self):
		pattern = re.compile('(?<=地) *?(?=址)|(?<=住) *?(?=所)|(?<=坐) *?(?=落)|(?<=住) *?(?=址)')
		self.strings = pattern.sub('', self.strings)
		pattern = re.compile('(?<=地址|住所|坐落|住址)[:：] *?[\w（）()]+')
		try:
			strings = pattern.findall(self.strings)[0]
			strings = clean_data(strings, pattern_str='\w', method='search')
		except:
			strings = ''
		return strings

	def searchBPiece(self):
		pattern = re.compile('(?<=地) *?(?=址)|(?<=住) *?(?=所)|(?<=坐) *?(?=落)|(?<=住) *?(?=址)')
		self.strings = pattern.sub('', self.strings)
		pattern = re.compile('(?<=地址|住所|坐落|住址)[:：] *?[\w（）()]+')
		try:
			strings = pattern.findall(self.strings)[1]
			strings = clean_data(strings, pattern_str='\w', method='search')
		except:
			strings = ''
		return strings
	# @pd_output_str
	# def searchAAndBPiece(self, lis='main'):
	#
	# 	pattern = re.compile('(?<=地) *?(?=址)|(?<=住) *?(?=所)|(?<=坐) *?(?=落)|(?<=住) *?(?=址)')
	# 	self.df[lis] = list(map(lambda x: pattern.sub('', x) if pd.notna(x) and pattern.search(x)!=None else x, self.df[lis]))
	# 	pattern = re.compile('(?<=地址|住所|坐落|住址)[:：] *?[\w（）()]+')
	# 	self.df['APiece'] = list(map(lambda x: pattern.findall(x)[0] if pd.notna(x) and pattern.search(x)!=None else np.nan, self.df[lis]))
	# 	self.df['BPiece'] = list(map(lambda x: pattern.findall(x)[1] if pd.notna(x) and pattern.search(x)!=None else np.nan, self.df[lis]))
	# 	self.df = clean_data(self.df, col='APiece', pattern_str='\w', method='search')
	# 	self.df = clean_data(self.df, col='BPiece', pattern_str='\w', method='search')
	#
	# 	return self.df

	# 税务登记号
	# @pd_output_str
	# def searchAAndBTaxNumber(self, lis='main'):
	#
	# 	pattern = re.compile('(?<=纳税人识别号)[:： ]*?[\da-zA-Z ]{15,20}|(?<=税务登记号)[:： ]*?[\da-zA-Z ]{15,20}')
	# 	self.df['ATax'] = list(map(lambda x: pattern.findall(x)[0] if pd.notna(x) and pattern.search(x)!=None else np.nan, self.df[lis]))
	# 	self.df['BTax'] = list(map(lambda x: pattern.findall(x)[1] if pd.notna(x) and pattern.search(x)!=None else np.nan, self.df[lis]))
	#
	# 	return self.df

	def searchATaxNumber(self):

		pattern = re.compile('(?<=纳税人识别号)[:： ]*?[\da-zA-Z ]{15,20}|(?<=税务登记号)[:： ]*?[\da-zA-Z ]{15,20}')
		try:
			strings = pattern.findall(self.strings)[0]
			strings = clean_data(strings, pattern_str='\d', method='search')
		except:
			strings = ''
		return strings

	def searchBTaxNumber(self):

		pattern = re.compile('(?<=纳税人识别号)[:： ]*?[\da-zA-Z ]{15,20}|(?<=税务登记号)[:： ]*?[\da-zA-Z ]{15,20}')
		try:
			strings = pattern.findall(self.strings)[1]
			strings = clean_data(strings, pattern_str='\d', method='search')
		except:
			strings = ''
		return strings

	# 银行账号
	# @pd_output_str
	# def searchAAndBBankNumber(self, lis='main'):
	#
	# 	pattern = re.compile('[账号]+[:： ]*?[\d ]{15,20}')
	# 	pattern1 = re.compile('[开户支付行]+[:： ]*?[\w ]+')
	# 	self.df['ABank'] = list(map(lambda x: pattern.findall(x)[0] if pd.notna(x) and pattern.search(x)!=None else np.nan, self.df[lis]))
	# 	self.df['ABankType'] = list(map(lambda x: pattern1.findall(x)[0] if pd.notna(x) and pattern1.search(x)!=None else np.nan, self.df[lis]))
	# 	self.df['BBank'] = list(map(lambda x: pattern.findall(x)[1] if pd.notna(x) and pattern.search(x)!=None else np.nan, self.df[lis]))
	# 	self.df['BBankType'] = list(map(lambda x: pattern1.findall(x)[1] if pd.notna(x) and pattern1.search(x)!=None else np.nan, self.df[lis]))
	#
	# 	return self.df

	def searchABankNumber(self):

		pattern = re.compile('[账号]+[:： ]*?[\d ]{15,20}')
		try:
			strings = pattern.findall(self.strings)[0]
			strings = clean_data(strings, pattern_str='\d', method='search')
		except:
			strings = ''
		return strings

	def searchBBankNumber(self):

		pattern = re.compile('[账号]+[:： ]*?[\d ]{15,20}')
		try:
			strings = pattern.findall(self.strings)[1]
			strings = clean_data(strings, pattern_str='\d', method='search')
		except:
			strings = ''
		return strings

	def searchABankType(self):

		pattern = re.compile('[开户支付行]+[:： ]*?[\w ]+')
		try:
			strings = pattern.findall(self.strings)[0]
			strings = clean_data(strings, pattern_str='\w', method='search')
		except:
			strings = ''
		return strings

	def searchBBankType(self):

		pattern = re.compile('[开户支付行]+[:： ]*?[\w ]+')
		try:
			strings = pattern.findall(self.strings)[1]
			strings = clean_data(strings, pattern_str='\w', method='search')
		except:
			strings = ''
		return strings

	# 签订地点
	# @pd_output_str
	def searchSignPlace(self, lis='main'):

		pattern = re.compile('签订地点[：: ]+\w+')
		try:
			strings = pattern.search(self.strings).group()
			strings = clean_data(strings, pattern_str='\w', method='search')
		except:
			strings = ''
		return strings
		# self.df['place_of_signing'] = list(map(lambda x: pattern.search(x).group() if pd.notna(x) and pattern.search(x) != None else np.nan, self.df[lis]))
		# self.df = clean_data(self.df, col='place_of_signing', pattern_str='\w', method='search')

		# return self.df

	# 签订时间
	# @pd_output_str
	def searchSignTime(self, lis='main', out_put_type='time'):

		# def searchDateMid(strings, pattern=''):
		#
		# 	pattern = re.compile('^\d+(\D+)')
		# 	pattern.search(strings).group()
		#
		# 	return

		pattern = re.compile('时 *?间[：: ][\d年月日时分秒\-]+|日 *?期[：: ][\d年月日时分秒\-]+')
		try:
			strings = pattern.search(self.strings).group()
			strings = clean_data(strings, pattern_str='\w', method='search')
		except:
			strings = None
		# date_str = '11n12/2023'
		if strings:
			print(strings)
			format_str = '%Y年%m月%d日'
			strings = datetime.datetime.strptime(strings, format_str)
		if out_put_type == 'string':
			if strings:
				strings = strings.strftime('%Y-%m-%d')
		return strings
		# self.df['time_of_signing'] = list(map(lambda x: pattern.search(x).group() if pd.notna(x) and pattern.search(x) != None else np.nan, self.df[lis]))
		# self.df = clean_data(self.df, col='time_of_signing', pattern_str='\w', method='search')
		#
		# return self.df

	# 交提货时间
	# @pd_output_str
	def searchDeliveryTime(self, lis='main'):

		pattern = re.compile('[交收][(提)（）]*?货时间[:： ]*?(合约签订)*?\w+')
		try:
			strings = pattern.search(self.strings).group()
			strings = clean_data(strings, pattern_str='\w', method='search')
		except:
			strings = ''
		return strings
		# self.df['delivery_time'] = list(map(lambda x: pattern.search(x).group() if pd.notna(x) and pattern.search(x) != None else np.nan, self.df[lis]))
		# self.df = clean_data(self.df, col='delivery_time', pattern_str='\d', method='search')
		#
		# return self.df

	# 交提货地点
	# @pd_output_str
	def searchDeliveryPlace(self, lis='main'):
		pattern_place = re.compile('.+[省市区街栋座层]+.*?(?=[\u4e00-\u9fa5])')
		pattern = re.compile('[交收][(提)（）]*?货.*?人[:： ]*?.*?([^:：]+)(?<=[\d])|[交收][(提)（）]*?货.*?人[:： ]*?.*?(\w+$)|[交收][(提)（）]*?货.*?地址[:： ]*?.*?(\w+$)')
		try:
			strings = re.sub('\n', '', pattern.search(self.strings).group())
			strings = clean_data(strings, pattern_str='\w', method='search')
		except:
			strings = ''
		try:
			strings = pattern_place.search(strings).group()
		except:
			strings = ''
		return strings

		# self.df['delivery_place'] = list(map(lambda x: pattern.search(x).group() if pd.notna(x) and pattern.search(x) != None else np.nan, self.df[lis]))
		# self.df = clean_data(self.df, col='delivery_place', pattern_str='\w', method='search')
		#
		# return self.df

	# 收货人
	# @pd_output_str
	def searchDeliveryPeople(self, lis='main'):

		pattern = re.compile('[交收][(提)（）]*?货.*?人[:： ]*?.*?([^:：]+)(?<=[\d])|[交收][(提)（）]*?货.*?人[:： ]*?.*?(\w+$)')
		try:
			strings = re.sub('\n', '', pattern.search(self.strings).group())
			strings = clean_data(strings, pattern_str='\w', method='search')
		except:
			strings = ''
		delivery_place = self.searchDeliveryPlace()
		delivery_place = self.searchDeliveryPlace()
		deliverer_phone = self.searchDeliveryPhone()
		strings = re.sub(delivery_place, '', strings)
		strings = re.sub(deliverer_phone, '', strings)
		# pattern = re.compile('.+?[省市区街镇县座层栋号].*?[^\d]+')
		# try:
		# 	strings = pattern.search(strings).group()
		# except:
		# 	strings = ''
		return strings
		# self.df['deliverer'] = list(map(lambda x: pattern.search(x).group() if pd.notna(x) and pattern.search(x) != None else np.nan, self.df[lis]))
		# self.df = clean_data(self.df, col='deliverer', pattern_str='\w', method='search')
		#
		# return self.df

	# 交货人联系方式
	# @pd_output_str
	def searchDeliveryPhone(self, lis='main'):

		pattern_place = re.compile('\d+$')
		pattern = re.compile('[交收][(提)（）]*?货.*?人[:： ]*?.*?([^:：]+)(?<=[\d])|[交收][(提)（）]*?货.*?人[:： ]*?.*?(\w+$)')
		try:
			strings = re.sub('\n', '', pattern.search(self.strings).group())
			strings = clean_data(strings, pattern_str='\w', method='search')
		except:
			strings = ''
		try:
			strings = pattern_place.search(strings).group()
		except:
			strings = ''
		return strings

		# self.df['deliverer_phone'] = list(map(lambda x: pattern.search(x).group() if pd.notna(x) and pattern.search(x) != None else np.nan, self.df[lis]))
		# self.df = clean_data(self.df, col='deliverer_phone', pattern_str='\w', method='search')
		#
		# return self.df

	# 争议解决方式
	def disputeResolutionMethod(self):

		pattern = re.compile('(?<=争议解决方[式法]：)[^一二三四五六七八九十]+|(?<=争议解决方[式法]:)[^一二三四五六七八九十]+')
		try:
			strings = pattern.search(self.strings).group()
			# strings = clean_data(strings, pattern_str='\w', method='search')
		except:
			strings = ''
		# strings, details = self.nlp(strings)
		# print(details)
		return strings

	# 付款方式
	def paymentMethod(self):

		pattern = re.compile('(?<=付款方式：)\w+|(?<=付款方式:)\w+')
		try:
			strings = pattern.search(self.strings).group()
			# strings = clean_data(strings, pattern_str='\w', method='search')
		except:
			strings = ''
		# strings, details = self.nlp(strings)
		# print(details)
		return strings

	# 临时抽取金额
	def select_money(self):

		pattern = re.compile('合 *?计[￥:$： \n]*[\d\.]+')
		try:
			strings = pattern.search(self.strings).group()
			# print(strings)
			strings = clean_data(strings, pattern_str='[\d\.]', method='search')
		except:
			strings = ''

		return strings

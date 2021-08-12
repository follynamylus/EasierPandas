
import pandas as pd # <-- Imported pandas package
from abc import ABC, abstractmethod, abstractproperty # <-- Imported ABC package from abc.



class AbstractClass(ABC):
	'''
ABSTRACT CLASS WHERE THE CONSTRUCTOR WAS INNITIATED
It inherits from abc python package and has all other class attributes and instance attributes declared in it.

	'''
	str_cols = [] # <-- Class level attributes which can be accessed by any instance and methods.
	int_cols = []
	float_cols = []
	sta = []
	tends = []
	ranges = []
	range_op = []
	col = []
	oper = []



	def __init__(self, data, *args, **kwargs): # <-- The constructor method which is called automatically anytime the class
	# instance is called.
		self.data = data # <-- The data instance attribute that stores data and is called in the constructor.
		self.read_data = pd.read_csv(f"{self.data}") # <-- This instance attribute reads in the data and stores it.
		self.cols_with_null = [] # <-- This instance list attribute stores columns with null values.
		self.cols_withno_null = [] # <-- This instance list attribute stores columns with no null values.
		self.miss_percent = [] # <-- This instance list attribute stores the % of missing values
		self.cols = [] # <-- This instance list attribute stores columns
		self.cols = self.read_data.columns # <-- This instance attribute stores columns read from the data
		self.list_cols = self.read_data.columns.to_list() # This converts data column to list and stores it.
		for col in self.list_cols: # This loops through the data column list
			if self.read_data[col].dtypes == 'int64': # This relates the type of the data column to integer data type
				Preparer.int_cols.append(col) # This appends the column to a class attribute if it returns true above
			elif self.read_data[col].dtypes == 'object': # This relates column to obj data type 
				Preparer.str_cols.append(col) # Then appends to str_cols class attribute if it returns true
			else :
				Preparer.float_cols.append(col) # This append remaining columns to to float_cols class attribute
		self.numerical = (Preparer.int_cols + Preparer.float_cols) # columns added together in the turple attr self.numerical
		for cols in self.numerical: # loops through the turple self.numerical
			Preparer.range_op.append(self.read_data[cols].max() - self.read_data[cols].min()) # Subtract minimum instance
			# in a cloumn from its max and appends to class attr range_op
			Preparer.col.append(cols) # appends column to class col attr
		self.ranged_item = {key : value for key , value in zip (tuple(Preparer.col), tuple(Preparer.range_op))} # <-- create
		# a dictionary by zipping two created turples together and save to self.ranged_item. 
		for cols in self.numerical: # Loop through self.numerical
			Preparer.oper.append(self.read_data[cols].mean() - self.read_data[cols].median()) # subtract mean from the median
		# of the data and append to oper
			Preparer.col.append(cols)
		self.dic_tends = {key : value for key , value in zip (tuple(Preparer.col), tuple(Preparer.oper))}# converts as done earlier
		for col in self.list_cols: # loop through list columns
			val = (self.read_data[col].isnull().sum()/ len(self.read_data)) * 100 # Gets percentage of the missing vals
			self.miss_percent.append(val) # Append it to list miss_percent
		@abstractmethod # <-- Abstract method decorator which made this an abstract class
		def printer(self):
			return print('Here is pandas ++')
			




class Preparer(AbstractClass):
	'''
THIS IS A GENERAL CLASS FOR PREPARING OUR DATA
We use and extend our pandas package to make data preparation and processing easier

	'''
	def show_data(self): # <-- A method that shows the data in data frame format
		df = self.read_data.head()
		return df

	def get_info(self): # <-- A function that shows the informations about the dataset
		info = self.read_data.info()
		return info
	 @property # <-- Decorator to make it a read only method.
	def show_columns(self): # <-- A function that shows colums
		print(type(self.cols))
		return self.cols
	@property
	def sort_columns(self): # <-- Method to display sorted columns into int, float and object. 
		return f'''
		Integer columns are : {Preparer.int_cols } 
		object columns are : {Preparer.str_cols }
		float columns are : {Preparer.float_cols}'''
	def values_missing(self): # <-- Method to check missing values
		Print_missing = []
		missing_vals = []
		list_cols = self.read_data.columns.to_list()
		for col in list_cols: 
			val = self.read_data[col].isnull().sum()
			missing_vals.append(val)
			print(f"In {col}, the missing values are {val} ")
		return f'''
		total columns is : {len(list_cols)}
		length of the data is : {len(self.read_data)}
		'''
	def null_values_bool(self): # <-- Method to check columns with missing values and those without
		missing_vals = []
		list_cols = self.read_data.columns.to_list()
		for col in list_cols: 
			val = self.read_data[col].isnull().sum()
			if val != 0 :
				self.cols_with_null.append(col)
			else :
				self.cols_withno_null.append(col)
		print(f'''columns with no null values are : {self.cols_withno_null}
__________________________________________________________________
columns with null values are : {self.cols_with_null}
				''')
		return f'''
		total columns with null values : {len(self.cols_with_null)}
		total columns with no null values : {len(self.cols_withno_null)}
		total columns is : {len(list_cols)}
		length of the data is : {len(self.read_data)}
		'''
	def percentage_missing(self): # <-- Method to check percentage of missing values
		print(f'Missing is {self.miss_percent}')
		return f'''
		total columns is : {len(self.list_cols)}
		total rows is : {len(self.read_data)}
		'''	
	def fill_with(self): # <-- for filling missing values appropriately 
		for col in self.list_cols: 
			val = (self.read_data[col].isnull().sum()/ len(self.read_data)) * 100
			self.miss_percent.append(val)
		filled_cols = {key : values for key, values in zip(self.cols, self.miss_percent)}
		for k , v in filled_cols.items():
			if self.read_data[k].dtypes == 'int64':
				if 0 < v <= 30.0 :
					self.read_data[k].fillna(self.read_data[k].median(), inplace = True)
				elif v > 30.0 :
					self.read_data.drop(k, axis = 1, inplace = True)
			elif self.read_data[k].dtypes == 'float64':
				if 0 < v <= 30.0 :
					self.read_data[k].fillna(self.read_data[k].median(), inplace = True)
				elif v > 30.0 :
					self.read_data.drop(k, axis = 1, inplace = True)
			elif self.read_data[k].dtypes == 'object':
				if 0 < v <= 30.0 :
					self.read_data[k].fillna(self.read_data[k].mode()[0], inplace = True)
				elif v > 30.0 :
					self.read_data.drop(k, axis = 1, inplace = True)
		return self.read_data.info()
	def per(self): # < -- This returns missing values
		return self.miss_percent
	def __repr__(self): # This method prints what the class is.
		return f'This is a Preparer class'

class Numerical(Preparer):
	'''
A CLASS FOR PROCESSING NUMERICAL DATA
It in herits from Preparer class and contains , statistical analysis, filling missing values and so on
	'''

	def __repr__(self):
		return f'THIS IS NUMERICAL CLASS'
	def fill_with(self): # <-- fills missing values
		filled_cols = {key : values for key, values in zip(self.cols, self.miss_percent)}
		for k , v in filled_cols.items():
			if self.read_data[k].dtypes == 'int64':
				if 0 < v <= 30.0 :
					self.read_data[k].fillna(self.read_data[k].median(), inplace = True)
				elif v > 30.0 :
					self.read_data.drop(k, axis = 1, inplace = True)
			elif self.read_data[k].dtypes == 'float64':
				if 0 < v <= 30.0 :
					self.read_data[k].fillna(self.read_data[k].median(), inplace = True)
				elif v > 30.0 :
					self.read_data.drop(k, axis = 1, inplace = True)
		return self.read_data.info()

	def Statis(self): # <-- Check for analysis
		for col in self.numerical:
			Preparer.sta.append(self.read_data[col].describe())
		return Preparer.sta

	def central_tends(self): # < -- check for central tendencies
		return self.dic_tends
	def ranges(self): # <-- check for range
		return self.ranged_item
	def varies(self): # < -- compares range to center tendencies to know a bit how skewed it is.
		column = []
		norm = []
		for cols in self.numerical:
			column.append(cols)
			norm.append(self.ranged_item[cols] / self.dic_tends[cols])
		dic_norm = {key : values for key , values in zip(tuple(column),tuple(norm))}
		return dic_norm

class Categorical(Preparer):
	'''
CLASS FOR PROCESSING CATEGORICAL DATA
It inherits from Preparer class and analysis categorical data.
	'''
	def __repr__(self):
		return "This is a categorical class"
	def fill_with(self): # < -- fill missing values.
		for col in self.list_cols: 
			val = (self.read_data[col].isnull().sum()/ len(self.read_data)) * 100
			self.miss_percent.append(val)
		filled_cols = {key : values for key, values in zip(self.cols, self.miss_percent)}
		for k , v in filled_cols.items():
			if self.read_data[k].dtypes == 'int64':
				if 0 < v <= 30.0 :
					pass
			elif self.read_data[k].dtypes == 'float64':
				pass
			elif self.read_data[k].dtypes == 'object':
				if 0 < v <= 30.0 :
					self.read_data[k].fillna(self.read_data[k].mode()[0], inplace = True)
				elif v > 30.0 :
					self.read_data.drop(k, axis = 1, inplace = True)
		return self.read_data.info()
	
	



		





#Num = Categorical(data = "autos.csv")



#print(Num.fill_with())
#print()
#help(Preparer)	
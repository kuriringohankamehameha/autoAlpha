import sys
import time
import PySimpleGUI as sg

import re, itertools

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

def min(a,b):
	if(a > b):
		return b
	else:
		return a


def string_hide(str, k):
    b = ""
    for i,j in enumerate(str):
        b = b + chr(ord(j) + k)
    return b

def string_reveal(str, k):
    b = ""
    for i,j in enumerate(str):
        b = b + chr(ord(j) - k)
    return b

def find_parameter_index_in_alpha(alpha, param_list):
	for index, parameter in enumerate(param_list):
		if parameter in alpha:
			return index
	return -1

def permute_string_across_parameters(text, no_of_inputs, param_list):
	#Example:
	#text = "((1)) give me something ((2))"

	keywords = {}
	#keywords["wouldyou"] = ["can you", "would you", "please"]
	#keywords["please"] = ["please", "ASAP"]

	#inputs = 2

	for i in range(int(no_of_inputs)):
		string = str(i+1)
		keywords[string] = param_list

	#keywords["allah1"] = ["open","close","top","bottom"]
	#keywords["allah2"] = ["open","close","top","bottom"]

	# Get a list of bracketed terms
	lsources = re.findall("\[\[(.*?)\]\]", text)

	# Build a list of the possible substitutions 
	ldests = []
	for source in lsources:
	    ldests.append(keywords[source])

	final_list_of_alphas = []

	# Generate the various pairings
	for lproduct in itertools.product(*ldests):
	    output = text
	    for src, dest in zip(lsources, lproduct):
	        # Replace each term (you could optimise this using a single re.sub)
	        output = output.replace("[[%s]]" % src, dest)

	    #print(output)
	    final_list_of_alphas.append(output)
	return final_list_of_alphas

class AlphaGenerator(object):
	def __init__(self, browser, filename):
		self.wait_time = 20
		self.max_num_concurrent_simulations = 4
		self.filename = filename
		self.browser = browser
		self.number_of_substitutions = 0
		self.alpha_list = []
		with open(filename, 'r') as file:
			self.alpha = file.readline()
			self.param_set = file.readline()
		form = sg.FlexForm('generateAlphas')  # begin with a blank form
		layout = [
		          [sg.Text('Please enter your primary Alpha: ')],
		          [sg.Text('Alpha', size=(15, 1)), sg.InputText(self.alpha)],
		          [sg.Text('Enter comma separated Parameter set (optional): ')],
		          [sg.Text('Parameter Set', size=(15, 1)), sg.InputText(self.param_set)],
		          [sg.Text('Please enter the number of substitutions you need: ')],
				  [sg.Text('No. of Substitutions', size=(15, 1)), sg.InputText(self.number_of_substitutions)],
		          [sg.Submit(), sg.Cancel()]
		         ]
		self.button, self.values = form.Layout(layout).Read()

		if self.button == 'Cancel' or self.button is None:
			exit(0) 

		self.alpha = self.values[0]
		self.param_set = self.values[1] 
		self.csv_parameters = self.values[1] #Remains Unchanged
		self.number_of_substitutions = self.values[2]

		self.list = []

	def setupDrivers(self):
		if self.browser == "Safari":
			self.driver = webdriver.Safari()
		elif self.browser == "Chrome":
			chrome_options = Options()
			chrome_options.add_argument("--disable-infobars")
			self.driver = webdriver.Chrome(executable_path = '/Users/ramachandran/Downloads/chromedriver',chrome_options=chrome_options)

	def assign_values_to_param_set(self, param_set):
		self.index = find_parameter_index_in_alpha(self.alpha, param_set)
		self.list = self.param_set.split(',')
		self.list[0] = self.list[0].replace('\n','')
		#index_list = find_parameter_index_in_alpha(self.alpha, self.list)
		index_list = 1

		if (self.button == 'Submit' and self.alpha == '') or (self.param_set != '\n' and index_list == -1) or (self.param_set == '' and self.index == -1):
			raise IOError("Invalid Alpha Entered")		
		if(self.param_set != '\n'):
			self.param_set = self.list
		else:
			self.param_set = param_set
			self.index = index_list

	def simulate_alphas(self):
		url = 'https://websim.worldquantvrc.com/sign-in'
		self.driver.get(url)
		time.sleep(4)
		email_id = self.driver.find_element_by_id("email")
		email_id.send_keys("ram.vijaykrishna@gmail.com")
		password = self.driver.find_element_by_id("password")
		password.send_keys(string_reveal("\x97¦©®¨¦±v", 69))
		login_button = self.driver.find_element_by_xpath("//*[@id='root']/div/section/div/article/div/div/form/div[4]/button")
		login_button.click()
		time.sleep(2)
		url = 'https://websim.worldquantvrc.com/simulate'
		self.driver.get(url)
		
		if self.browser == "Chrome":
			url = 'https://websim.worldquantvrc.com/simulate'
			self.driver.get(url)
		
		time.sleep(5)
		skip_tutorial = self.driver.find_element_by_xpath("/html/body/div[6]/div/div[5]/a[1]")
		skip_tutorial.click()
		time.sleep(4)
		curr = 0
		#alpha = "((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1 * 1))"
		
		dummy_alpha = self.alpha
		#self.param_set[0], self.param_set[self.index] = self.param_set[self.index], self.param_set[0] 

		highest_correlation = []

		self.alpha_list = permute_string_across_parameters(self.alpha, self.number_of_substitutions, self.param_set)
		
		while(curr < len(self.alpha_list)):
			click_editor = self.driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div/div[3]/div[2]/div/div[1]/div/div/div/div[1]/div/div[1]/textarea")
			click_editor.click()
			write_code = self.driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div/div[3]/div[2]/div/div[1]/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div[4]/div/span/span")
			time.sleep(2)
			#if curr != 0:
				#dummy_alpha = self.alpha.replace(self.param_set[0], self.param_set[curr])
			dummy_alpha = self.alpha_list[curr]
			#print(dummy_alpha)
			if self.browser == "Chrome":	
				write_code.click()
			ActionChains(self.driver).move_to_element(write_code).send_keys(dummy_alpha).perform()
			simulate_button = self.driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div/div[3]/div[3]/div[1]/div/div/button")
			simulate_button.click()
			next_button = self.driver.find_element_by_class_name('editor-tabs__new-tab-dropdown-element')
			next_button.click()
			time.sleep(20/min(self.max_num_concurrent_simulations,len(self.alpha_list)))
			curr += 1
		
		curr = 0
		tab_list = self.driver.find_elements_by_class_name('editor-tabs__tab-inside-element')
		
		while(curr < len(self.alpha_list)):
			ActionChains(self.driver).move_to_element(tab_list[curr]).click().perform()
			refresh_button = self.driver.find_element_by_xpath("//*[@id='alphas-correlation']/div[2]/div/div[1]/div[3]/div[2]")
			refresh_button.click()
			time.sleep(20/len(self.alpha_list))
			curr += 1
		
		curr = 0
		time.sleep(20)

		#Now go back to retrieve correlations and fetch the results
		print('Results : ')
		while(curr < len(self.alpha_list)):
			correlation = self.driver.find_element_by_xpath("//*[@id='alphas-correlation']/div[2]/div/div[1]/div[2]/div[2]")
			highest_correlation.append(correlation.text)
			print('****\n')
			print('For alpha :', self.alpha_list[curr], '\nHighest Correlation :', highest_correlation[curr])
			print('****\n')
			curr += 1

	def close_object(self, filename):
		with open(filename, "w") as file:
			file.write(self.alpha)
			file.write(self.csv_parameters)
		self.driver.close()

from django.test import TestCase
from website.models import *
from website.views import *
from django.http import HttpRequest

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time, os, socket
from datetime import datetime

#Test

class GUITest(StaticLiveServerTestCase):
	host = "127.0.0.1"
	port = 8000

	@classmethod
	def setUpClass(self):
		super(GUITest, self).setUpClass()
		geckodriver = "/Users/neli/Downloads/geckodriver"

		#Create screenshot current dir
		now = datetime.now()
		dt_string = now.strftime("%d%m%Y%H%M%S")
		self.screenshot_dir = "target/screenshots/unit/" + dt_string + "/"
		os.makedirs(self.screenshot_dir)

		socket.setdefaulttimeout(3000)
		options = Options()
		options.headless = True
		self.driver = webdriver.Firefox(executable_path=geckodriver,options=options)

		self.driver.set_window_size(1024, 600)
		self.driver.maximize_window()

	@classmethod
	def setUp(self):
		self.tax1 = Taxonomy(ncbi_id=9606,organism_name="Homo sapiens")
		self.tax1.save()
		self.tax2 = Taxonomy(ncbi_id=1758,organism_name="Canis lupus")
		self.tax2.save()
		
		self.gene = Gene(name="PLA2GA")
		self.gene.save()
		
		self.prot1 = UniprotKb(accession="P11111",sequence="AWCF",taxonomy=self.tax1,gene=self.gene)
		self.prot1.save()
		self.prot2 = UniprotKb(accession="P22222",sequence="PQRSTSC",taxonomy=self.tax1,gene=self.gene)
		self.prot2.save()
		self.prot3 = UniprotKb(accession="P33333",sequence="AAAAA",taxonomy=self.tax2,gene=self.gene)
		self.prot3.save()

	@classmethod
	def tearDownClass(self):
		self.driver.quit()
		super(GUITest, self).tearDownClass()

	def test_proteins(self):
		self.driver.get(str(self.live_server_url) + "/proteins")

		content = self.driver.find_element_by_id("content")
		items = content.find_elements_by_tag_name("li")

		try:
			self.assertEqual(len(items),3)
			self.assertEqual(items[0].text,"P11111")
			self.assertEqual(items[1].text,"P22222")
			self.assertEqual(items[2].text,"P33333")
		except Exception as exception:
			self.driver.save_screenshot(self.screenshot_dir + "proteins.png")
			raise AssertionError()
			

	def test_protein(self):
		self.driver.get(str(self.live_server_url) + "/protein/P11111")

		content = self.driver.find_element_by_id("content")

		try:
			title = content.find_element_by_tag_name("h1")
			self.assertEqual(title.text,"NomeErrado")

			sequence = content.find_elements_by_tag_name("p")[0]
			self.assertEqual(sequence.text,"AWCF")

			links = content.find_elements_by_tag_name("a")
			self.assertEqual(links[0].text,"Homo sapiens (9606)")
			self.assertEqual(links[0].get_attribute("href"),str(self.live_server_url) + "/taxonomy/9606/")
			self.assertEqual(links[1].text,"PLA2GA")
			self.assertEqual(links[1].get_attribute("href"),str(self.live_server_url) + "/gene/PLA2GA/")
		except Exception as exception:
			self.driver.save_screenshot(self.screenshot_dir + "protein.png")
			#raise ValueError("Protein failed")
			raise AssertionError()

# Create your tests here.
class WebsiteTest(TestCase):
	@classmethod
	def setUpClass(self):
		#Cria modelos virtuais
		super(WebsiteTest, self).setUpClass()

		self.tax1 = Taxonomy(ncbi_id=9606,organism_name="Homo sapiens")
		self.tax1.save()
		self.tax2 = Taxonomy(ncbi_id=1758,organism_name="Canis lupus")
		self.tax2.save()
		
		self.gene = Gene(name="PLA2GA")
		self.gene.save()
		
		self.prot1 = UniprotKb(accession="P11111",sequence="AWCF",taxonomy=self.tax1,gene=self.gene)
		self.prot1.save()
		self.prot2 = UniprotKb(accession="P22222",sequence="PQRSTSC",taxonomy=self.tax1,gene=self.gene)
		self.prot2.save()
		self.prot3 = UniprotKb(accession="P33333",sequence="AAAAA",taxonomy=self.tax2,gene=self.gene)
		self.prot3.save()

	@classmethod
	def tearDownClass(self):
		#Destroi modelos virtuais
		super(WebsiteTest, self).tearDownClass()

	def test_model_protein(self):
		#Length
		self.assertEqual(self.prot1.length,4)
		self.assertEqual(self.prot2.length,7)
		self.assertEqual(self.prot3.length,5)

		#__str__
		self.assertEqual(str(self.prot1),"P11111")
		self.assertEqual(str(self.prot2),"P22222")
		self.assertEqual(str(self.prot3),"P33333")

	def test_getHumanProteins(self):
		proteins = getHumanProteins()
		
		self.assertEqual(len(proteins),2)
		self.assertIn(self.prot1,proteins)
		self.assertIn(self.prot2,proteins)
		self.assertNotIn(self.prot3,proteins)

	def test_views(self):
		request = HttpRequest()

		response = proteins(request)
		self.assertEqual(response.status_code,200)

		response = protein(request,"P11111")
		self.assertEqual(response.status_code,200)






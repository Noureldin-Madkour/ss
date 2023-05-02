# Copyright (c) 2023, Nour and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from docx import Document as docx
from docxtpl import DocxTemplate
from frappe.utils import get_site_name 
import os
import json
import webbrowser
from frappe.utils import cstr

class FillingRequest(Document):
	pass

@frappe.whitelist()
def download_file(doc):
	frappe.throw("SSS")
	doc = json.loads(doc)
	get_template = frappe.db.sql(f"""
			select * from `tabTemplate`
			join `tabTemplate Table` on `tabTemplate`.name = `tabTemplate Table`.parent
			where `tabTemplate Table`.doctype_name = '{doc['doctype']}'
			and `tabTemplate Table`.template_file IS NOT NULL
	""",as_dict = 1)
	if get_template is None:
		frappe.throw("There is no such template for this doctype")
	
	current_working_directory = os.getcwd()
	filee = frappe.get_doc("File", get_template[0].template_file)
	template = DocxTemplate(filee.get_full_path())
	to_fill_in = doc
	template.render(to_fill_in)

	# save the modified document
	template.save(frappe.get_site_path()+ '/public/files' + '/filling_request.docx')
	
	
	file_doc = frappe.get_doc({
		'doctype': 'File',
		'file_name': 'filling_request.docx',
		'file_url': '/files/filling_request.docx',
		'is_private': 0,
	})

	# Insert the new document
	file_doc.insert()
	
	# site_name = get_site_name(frappe.local.request.host)
	# port_number = frappe.local.conf.get('webserver_port')
	# site_url = str(site_name) + ':' + str(port_number)
	# webbrowser.open_new(site_url + '/files/filling_request.docx')

	
	





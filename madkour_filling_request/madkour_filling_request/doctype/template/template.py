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

class Template(Document):
	pass

@frappe.whitelist()
def download_file(doc):
	doc = json.loads(doc)
	print(doc)
	get_template = frappe.db.sql(f"""
			select * from `tabTemplate`
			join `tabTemplate Table` on `tabTemplate`.name = `tabTemplate Table`.parent
			where `tabTemplate Table`.doctype_name = '{doc['doctype']}'
			and `tabTemplate Table`.template_file IS NOT NULL
	""",as_dict = 1)
	if get_template is None:
		frappe.throw("There is no such template for this doctype")

	current_working_directory = os.getcwd()
	data = frappe.db.sql(f"""
			select 
			full_name,
			mobile_number,
			project_name,
			received_national_id,
			address,
			unit_title,
			received_name,
			received_phone_number
					
			from `tabFilling Request`
			where name = '{doc['name']}'
	""",as_dict = 1)
	
	if data:
		
		data = data[0]
	else:
		frappe.throw("Save the Doctype")
	
	
	d = data
	for key, value in d.items():
			if value ==  '':
				d[key] is None
	


	filee = frappe.get_doc("File", get_template[0].template_file)
	head, tail = os.path.split(filee.get_full_path())
	current_file_name = doc['doctype'] + '_' + doc['name'] + '_' + tail
	template = DocxTemplate(filee.get_full_path())
	to_fill_in = data
	template.render(to_fill_in)
	file_doc = {}
	for key, value in doc.items():
		for key1, value1 in d.items():
			if key == key1:
				if value != value1:
					frappe.throw("Save the Doctype")

	if not frappe.db.exists("File", {"file_name": current_file_name}):
		# save the modified document
		template.save(filename = frappe.get_site_path()+ '/private/files/inprogress_' + current_file_name)
		file_doc = frappe.get_doc({
		'doctype': 'File',
		'file_name': current_file_name,
		'file_url': '/private/files/inprogress_'+ current_file_name,
		'is_private': 1,
		})

		# Insert the new document
		file_doc.insert()
		os.remove(frappe.get_site_path()+ '/private/files/inprogress_' + current_file_name) 
	else :
		print("=====Start Getting File =====")
		file_doc = frappe.get_last_doc("File",filters={"file_name": current_file_name})
		print(file_doc)
		template.save(filename = frappe.get_site_path()+ '/private/files/' + current_file_name)

	return file_doc

	

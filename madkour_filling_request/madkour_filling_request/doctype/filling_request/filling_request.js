// Copyright (c) 2023, Nour and contributors
// For license information, please see license.txt

frappe.ui.form.on('Filling Request', {


	download_file: function(frm) {
		download_file: {
			 frappe.call({
				args: {
					"doc" : frm.doc
				},
				method: "madkour_filling_request.madkour_filling_request.doctype.template.template.download_file",
				callback: function(r) {
					//frm.refresh_fields();
					//frm.refresh();
					console.log(r.message.file_name)
					let file_url = "/private/files/"+r.message.file_name;
					file_url = file_url.replace(/#/g, "%23");
					window.open(file_url);
				}
			})/*.then(msg => {
				let file_url = "/files/filling_request.docx";
				file_url = file_url.replace(/#/g, "%23");
				window.open(file_url);
			});*/
		}
	}
	
});

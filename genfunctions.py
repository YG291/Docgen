from docx import Document
from docx.text.run import Run
from docx.text.paragraph import Paragraph
from docx.table import Table
from pathlib import Path
from typing import Any

from doc_gen import Doc
from doc_gen import template_path

def directors_resolutions(global_dict: dict, people: dict):
    path = template_path("Directors_ Resolutions", "initial directors resolution.docx")
    doc = Doc(path, global_dict, people)
    doc.replace_main(global_dict)
    sale_table = doc.find_table_by_text('[BUYER]')
    for person in people['shareholders']:
        new_row = doc.copy_row(sale_table, 1)
        for cell in new_row.cells:
            for p in cell.paragraphs:
                doc._replace_p(p, people['shareholders'][person], '[BUYER]')
                doc._replace_p(p, people['shareholders'][person], '[COUNT]')
                doc._replace_p(p, people['shareholders'][person], '[PRICE]')
    doc.remove_row(sale_table, 1)
    doc.fill_signatures(people['directors'])
    doc.save_doc("Directors_ Resolutions", "initial directors resolution.docx")

def indemnification_agreement(global_dict: dict, people: dict):
    for person in people['directors']:
        path = template_path("Indemnification", "indemnification agreement.docx")
        doc = Doc(path, global_dict, people)
        doc.replace_main(global_dict)
        doc.replace_tables(global_dict)
        doc.replace_tables(people['directors'][person])
        doc.replace_main(people['directors'][person])
        doc.save_doc("Indemnification", "indemnification "+person+" .docx")
    
    for person in people['officers']:
        path = template_path("Indemnification", "indemnification agreement.docx")
        doc = Doc(path, global_dict, people)
        doc.replace_main(global_dict)
        doc.replace_main(people['officers'][person])
        doc.replace_tables(global_dict)
        doc.replace_tables(people['officers'][person])
        doc.save_doc("Indemnification", "indemnification "+person+" .docx")

def bylaws(global_dict: dict, people: dict):
    path = template_path("By-Laws", "bylaws.docx")
    doc = Doc(path, global_dict, people)
    doc.replace_main(global_dict)
    doc.save_doc("By-Laws", "bylaws.docx")

    path = template_path("By-Laws", "certificate of secretary.docx")
    doc = Doc(path, global_dict, people)
    doc.replace_main(global_dict)
    doc.replace_tables(global_dict)
    doc.save_doc("By-Laws", "certificate of secretary.docx")

    path = template_path("By-Laws", "incorporation certificate.docx")
    doc = Doc(path, global_dict, people)
    doc.replace_main(global_dict)
    doc.save_doc("By-Laws", "incorporation certificate.docx")

def ipassignment(global_dict: dict, people: dict):
    path = template_path("IP Assignments", "ip assignment.docx")
    for person in people['ip']:
        doc = Doc(path, global_dict, people)
        doc.replace_hf(global_dict)
        doc.replace_hf(people['ip'][person])
        doc.replace_main(global_dict)
        doc.replace_main(people['ip'][person])
        doc.replace_tables(people['ip'][person])
        doc.replace_tables(global_dict)
        p = doc.doc.paragraphs[len(doc.doc.paragraphs)-1]
        doc.dot_jots(p, people['ip'][person]['item_list'])
        doc.save_doc("IP Assignments", "ip assignment "+person+" .docx")

def jointescrow(global_dict: dict, people: dict):
     path = template_path("Joint Escrow Instructions", "joint escrow instructions.docx")
     for person in people['shareholders']:
        doc = Doc(path, global_dict, people)
        doc.replace_hf(global_dict)
        doc.replace_hf(people['shareholders'][person])
        doc.replace_main(global_dict)
        doc.replace_main(people['shareholders'][person])
        doc.replace_tables(people['shareholders'][person])
        doc.replace_tables(global_dict)
        doc.save_doc("Joint Escrow Instructions", "joint escrow "+person+" .docx")

def restrictedpurchase(global_dict: dict, people: dict):
    path = template_path("Restricted Stock Purchase", "restricted stock purchase agreement.docx")
    for person in people['shareholders']:
        doc = Doc(path, global_dict, people)
        doc.replace_hf(global_dict)
        doc.replace_hf(people['shareholders'][person])
        doc.replace_main(global_dict)
        doc.replace_main(people['shareholders'][person])
        doc.replace_tables(people['shareholders'][person])
        doc.replace_tables(global_dict)
        doc.save_doc("Restricted Stock Purchase", "restricted stock purchase "+person+" .docx")

def stock_assignment(global_dict: dict, people: dict):
    path = template_path("Restricted Stock Purchase", "stock assignment.docx")
    for person in people['shareholders']:
        doc = Doc(path, global_dict, people)
        doc.replace_main(global_dict)
        doc.replace_main(people['shareholders'][person])
        doc.replace_tables(people['shareholders'][person])
        doc.replace_tables(global_dict)
        doc.save_doc("Restricted Stock Purchase", "stock assignment "+person+" .docx")

def shareholder_resolution(global_dict: dict, people: dict):
    path = template_path("Shareholders_ Resolutions", "shareholders resolutions.docx")
    doc = Doc(path, global_dict, people)
    doc.replace_main(global_dict)
    doc.fill_signatures(people['shareholders'])
    doc.replace_tables(global_dict)
    doc.save_doc("Shareholders_ Resolutions", "shareholders resolutions.docx")

def stock_certificates(global_dict: dict, people: dict):
    counter = 1
    for person in people['shareholders']:
        path = template_path("Stock Certificates", "stock certificates.docx")
        doc = Doc(path, global_dict, people)
        doc.replace_main(global_dict)
        doc.replace_main(people['shareholders'][person])
        doc.replace_tables(people['shareholders'][person])
        doc.replace_tables(global_dict)
        doc.replace_tables({'[CERTNUM]': str(counter)})
        doc.save_doc("Stock Certificates", "stock certificate "+person+" .docx")
        counter += 1

def stock_purchase_agreement(global_dict: dict, people: dict):
    for person in people['shareholders']:
        path = template_path("Stock Purchase Agreement", "stock purchase agreement.docx")
        doc = Doc(path, global_dict, people)
        doc.replace_main(global_dict)
        doc.replace_main(people['shareholders'][person])
        doc.replace_tables(people['shareholders'][person])
        doc.replace_tables(global_dict)
        doc.save_doc("Stock Purchase Agreement", "stock purchase agreement "+person+" .docx")


if __name__ == '__main__':
    # The Global Dictionary for company-wide constants
    global_dict = {
        '[INCDATE]': 'January 15, 2026',
        '[DATE]': 'January 15, 2026',
        '[COMPANY]': 'Nexus Tech Solutions, Inc.',
        '[CORP]': 'Nexus Tech Solutions, Inc.',
        '[CEO]': 'Sarah Chen',
        '[PRES]': 'Sarah Chen',
        '[CFO]': 'Marcus Thorne',
        '[SECRETARY]': 'Elena Rodriguez',
        '[CLINE1]': '123 Innovation Way',
        '[CLINE2]': 'San Francisco, CA 94105',
        '[REGNAME]': 'Registered Agents Inc.',
        '[REGADD]': '456 Business Park Dr, Suite 10, San Francisco, CA 94105',
        '[AUTHTOTAL]': '10,000,000'
    }

    # The People Dictionary for individual-specific data
    people = {
        'directors': {
            'Sarah Chen': {
                '[DIRECTOR]': 'Sarah Chen',
                '[INDEMNITEE]': 'Sarah Chen',
                '[ILINE1]': '123 Innovation Way',
                '[ILINE2]': 'San Francisco, CA 94105'
            },
            'Marcus Thorne': {
                '[DIRECTOR]': 'Marcus Thorne',
                '[INDEMNITEE]': 'Marcus Thorne',
                '[ILINE1]': '789 Oak Lane',
                '[ILINE2]': 'Palo Alto, CA 94301'
            }
        },
        'shareholders': {
            'Sarah Chen': {
                '[BUYER]': 'Sarah Chen',
                '[COUNT]': '5,000,000',
                '[PRICE]': '500.00',
                '[BLINE1]': '123 Innovation Way',
                '[BLINE2]': 'San Francisco, CA 94105',
                '[BEMAIL]': 'sarah@nexustech.io'
            },
            'Venture Core Partners': {
                '[BUYER]': 'Venture Core Partners, LP',
                '[COUNT]': '1,000,000',
                '[PRICE]': '100.00',
                '[BLINE1]': '500 Market St',
                '[BLINE2]': 'San Francisco, CA 94104',
                '[BEMAIL]': 'admin@venturecore.com'
            }
        },
        'officers': {
            'Elena Rodriguez': {
                '[INDEMNITEE]': 'Elena Rodriguez',
                '[ILINE1]': '101 Pine Street',
                '[ILINE2]': 'Oakland, CA 94607'
            }
        },
        'ip': {
            'Sarah Chen': {
                '[ASSIGNOR]': 'Sarah Chen',
                'item_list': [
                    'Proprietary cloud computing architecture',
                    'Distributed ledger synchronization algorithm',
                    'User interface design patterns for Nexus v1.0'
                ]
            },
            'Marcus Thorne': {
                '[ASSIGNOR]': 'Marcus Thorne',
                'item_list': [
                    'Mobile application source code',
                    'API documentation and integration protocols'
                ]
            }
        }
    }
    directors_resolutions(global_dict, people)
    indemnification_agreement(global_dict, people)
    bylaws(global_dict, people)
    ipassignment(global_dict, people)
    jointescrow(global_dict, people)
    restrictedpurchase(global_dict, people)
    stock_assignment(global_dict, people)
    shareholder_resolution(global_dict, people)
    stock_certificates(global_dict, people)
    stock_purchase_agreement(global_dict, people)
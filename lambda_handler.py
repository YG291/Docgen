import json
from genfunctions import *

def fix_alias(dict_var: dict, aliases: list) -> None:
    for tup in aliases:
        if tup[0] in dict_var and tup[1] not in dict_var:
            dict_var[tup[1]] = dict_var[tup[0]]
def payload_to_dicts(payload):
    fields = payload.get('data', {}).get('fields', [])
    global_dict = {}
    person_entries = []
    current_person = None

    for f in fields:
        label = str(f.get('label', '')).strip()
        val = f.get('value', "")
        
        # 1. SKIP NULLS
        if val is None or val == "" or val is False:
            continue

        # 2. START NEW PERSON (The "Birth" of the record)
        if label == 'Name':
            current_person = {
                'Name': str(val),
                'item_list': [],
                # HARD-FIX: Inject the Buyer/Shareholder/Director tags IMMEDIATELY
                '[BUYER]': str(val),
                '[SHAREHOLDER]': str(val),
                '[DIRECTOR]': str(val),
                '[OFFICER]': str(val),
                '[ASSIGNOR]': str(val),
                '[INDEMNITEE]': str(val)
            }
            person_entries.append(current_person)
            continue 

        # 3. ATTACH DATA
        if current_person is not None:
            if label == 'Type' and isinstance(val, list):
                # RE-BUILD IDs locally for every person
                current_opts = {o['id']: o['text'].lower().strip() for o in f.get('options', [])}
                current_person['Type'] = ",".join([current_opts[i] for i in val if i in current_opts])
            
            elif label == 'item_list':
                current_person['item_list'] = [i.strip() for i in str(val).split(';') if i.strip()]
            
            elif label.startswith('['):
                current_person[label] = str(val)
        
        # 4. GLOBAL DATA
        if label.startswith('[') and (current_person is None or label in ['[CORP]', '[COMPANY]', '[DATE]', '[INCDATE]']):
            global_dict[label] = str(val)

    # 5. BUCKETING (The Address & Role Finalization)
    people = {'directors': {}, 'shareholders': {}, 'officers': {}, 'ip': {}}
    for row in person_entries:
        name = row.get('Name')
        type_str = row.get('Type', '')
        if not type_str: continue 
        
        roles = [r.strip() for r in type_str.split(',') if r.strip()]
        
        for role in roles:
            if role in people:
                role_data = row.copy()
                
                # ADDRESS FIX: Map [ALINE] to [ILINE] for Directors/Officers
                if role in ['directors', 'officers']:
                    if '[ALINE1]' in role_data: role_data['[ILINE1]'] = role_data['[ALINE1]']
                    if '[ALINE2]' in role_data: role_data['[ILINE2]'] = role_data['[ALINE2]']
                
                # ADDRESS FIX: Map [ALINE] to [BLINE] for Shareholders
                elif role == 'shareholders':
                    if '[ALINE1]' in role_data: role_data['[BLINE1]'] = role_data['[ALINE1]']
                    if '[ALINE2]' in role_data: role_data['[BLINE2]'] = role_data['[ALINE2]']
                
                people[role][name] = role_data

    # Final Global Sync
    if '[INCDATE]' in global_dict: global_dict['[DATE]'] = global_dict['[INCDATE]']
    if '[CORP]' in global_dict: global_dict['[COMPANY]'] = global_dict['[CORP]']

    return global_dict, people

def handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        global_dict, people = payload_to_dicts(body)
        
        # This will now show the correct count in your logs
        print(f"Final Count: {len(people['directors'])} Directors, {len(people['shareholders'])} Shareholders")

        # Run all generation functions
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
        
        return {"statusCode": 200, "body": "Success"}
    except Exception as e:
        print(f"Handler Error: {str(e)}")
        return {"statusCode": 500, "body": str(e)}
import csv

def fix_alias(dict_var: dict, aliases: list[tuple]) -> None:
    for tup in aliases:
        if tup[0] in dict_var and tup[1] not in dict_var:
            dict_var[tup[1]] = dict_var[tup[0]]


def load_data_from_csv(global_csv_path, people_csv_path):
    # 1. Load Global Dict
    global_dict = {}
    with open(global_csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) # Skip header
        for row in reader:
            if row: global_dict[row[0]] = row[1]
    general_aliases = [('[INCDATE]', '[DATE]'), ('[CORP]', '[COMPANY]')]
    fix_alias(global_dict, general_aliases)

    # 2. Load People Dict
    people = {'directors': {}, 'shareholders': {}, 'officers': {}, 'ip': {}}
    with open(people_csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Name']
            roles = [r.strip() for r in row['Type'].split(',')]
            
            raw_data = {k: v for k, v in row.items() if v and k not in ['Name', 'Type', 'item_list']}
            raw_data['namevariable*'] = name
            
            director_aliases = [('namevariable*', '[DIRECTOR]'), ('namevariable*', '[INDEMNITEE]'), 
                                ('namevariable*', '[ASSIGNOR]'), ('[ALINE1]', '[ILINE1]'), ('[ALINE2]', '[ILINE2]')]
            officer_aliases = [('namevariable*', '[INDEMNITEE]'), ('namevariable*', '[ASSIGNOR]'), 
                                ('[ALINE1]', '[ILINE1]'), ('[ALINE2]', '[ILINE2]')]
            shareholder_aliases = [('namevariable*', '[ASSIGNOR]'), ('[ALINE1]', '[BLINE1]'), ('[ALINE2]', '[BLINE2]'), ('namevariable*', '[BUYER]')]
            
            # Map the block to the correct roles with ISOLATION
            for role in roles:
                if role in people:
                    # CRITICAL: .copy() creates a unique dictionary for this specific role
                    role_data = raw_data.copy()
                    
                    # Apply specific aliases based on the role CURRENTLY being processed
                    if role == 'directors':
                        fix_alias(role_data, director_aliases)
                    elif role == 'officers':
                        fix_alias(role_data, officer_aliases)
                    elif role == 'shareholders':
                        fix_alias(role_data, shareholder_aliases)
                    elif role == 'ip':
                        # Handle item_list only for the IP role to keep other dicts small
                        if row.get('item_list'):
                            role_data['item_list'] = [i.strip() for i in row['item_list'].split(';')]
                        role_data['[ASSIGNOR]'] = name

                    # Save the unique, aliased dictionary into the specific bucket
                    people[role][name] = role_data

    return global_dict, people
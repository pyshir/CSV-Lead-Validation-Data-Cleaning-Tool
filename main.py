import csv
from pyShir_email import EmailValidation
import phonenumbers
# import json

email_validation = EmailValidation()

class DataBase:
    def __init__(self):
        self.valid_data = []
        self.invalid_data = []
        self.unique_emails = []
        self.duplicate_data = []
        self.unique_phone = []
        self.total_leads = 0

class DataValidation:

    def phone(self, number):
        try:
            number = phonenumbers.parse(number, 'BD')
            return(phonenumbers.is_valid_number(number))
        except:
            return False
            
class Counter:

    def duplicate_counter(self, duplicate_data):
        unique_item = []
        unique_id = []
        for i in duplicate_data:
            if i['lead_id'] in unique_id:
                continue
            else:
                unique_item.append(i)
                unique_id.append(i['lead_id'])

        return unique_item

    def add_item(self, main_dict, extra): # main_dict = {a:1, b:2,...}, extra = {c:3}
        return {**main_dict, **extra}


database = DataBase()
data_val = DataValidation()
counter = Counter()


try:
    with open("input_leads.csv", 'r', newline = "", encoding = "utf-8") as f:

        reader = csv.DictReader(f)

        

        for i in reader:

            validation = True

            database.total_leads += 1


            # Email check
            if i['email']:
                i['email'] = i['email'].replace(' ', '').strip().lower()
                result = email_validation.check(i['email'])
                if result:
                    if i['email'] in database.unique_emails:
                        av_bc = True
                        for bc in database.duplicate_data:
                            if bc['lead_id'] == i['lead_id']:
                                bc['Duplicate by'].append('email')
                                validation = False
                                av_bc = False
                                break
                        if av_bc:
                            x = {'Duplicate by': ['email']}
                            x_a = counter.add_item(i, x)
                            database.duplicate_data.append(x_a)
                            validation =  False
                    else:
                        database.unique_emails.append(i['email'])
                else:
                    av_ab = True
                    for ab in database.invalid_data:
                        if ab['lead_id'] == i['lead_id']:
                            ab['Reason'].append('Invalid Email')
                            validation = False
                            av_ab = False
                            break
                    if av_ab:
                        y = {'Reason': ['Invalid Email']}
                        y_a = counter.add_item(i, y)
                        database.invalid_data.append(y_a)
                        validation = False          
            else:
                av_ab = True
                for ab in database.invalid_data:
                    if ab['lead_id'] == i['lead_id']:
                        ab['Reason'].append('Blank Email')
                        validation = False
                        av_ab =  False
                        break
                if av_ab:
                    z = {'Reason': ['Blank Email']}
                    z_a = counter.add_item(i, z)
                    database.invalid_data.append(z_a)
                    validation = False

            # Phone check
            if i['phone']:
                i['phone'] = i['phone'].strip()
                if data_val.phone(i['phone']):
                    if i['phone'] in database.unique_phone:
                        av_bc = True
                        for bc in database.duplicate_data:
                            if bc['lead_id'] == i['lead_id']:
                                bc['Duplicate by'].append('phone')
                                validation = False
                                av_bc = False
                                break
                        if av_bc:
                            a = {'Duplicate by': ['phone']}
                            a_a = counter.add_item(i, a)
                            database.duplicate_data.append(a_a)
                            validation = False
                    else:
                        database.unique_phone.append(i['phone'])
                else:
                    av_ab = True
                    for ab in database.invalid_data:
                        if ab['lead_id'] == i['lead_id']:
                            ab['Reason'].append('Invalid Phone')
                            validation = False
                            av_ab = False
                            break
                    if av_ab:
                        b = {'Reason': ['Invalid Phone']}
                        b_a = counter.add_item(i, b)
                        database.invalid_data.append(b_a)
                        validation = False
            else:
                av_ab = True
                for ab in database.invalid_data:
                    if ab['lead_id'] == i['lead_id']:
                        ab['Reason'].append('Blank Phone')
                        validation = False
                        av_ab = False
                        break
                if av_ab:
                    c = {'Reason': ['Blank Phone']}
                    c_a = counter.add_item(i, c)
                    database.invalid_data.append(c_a)
                    validation = False

            # Amount check
            if i['amount']:
                x = i['amount'].strip()
                try:
                    float(x)
                except:
                    av_ab = True
                    for ab in database.invalid_data:
                        if ab['lead_id'] == i['lead_id']:
                            ab['Reason'].append('Invalid amount')
                            validation = False
                            av_ab = False
                            break
                    if av_ab:
                        p = {'Reason': ['Invalid amount']}
                        p_a = counter.add_item(i, p)
                        database.invalid_data.append(p_a)
                        validation = False
            else:
                av_ab = True
                for ab in database.invalid_data:
                    if ab['lead_id'] == i['lead_id']:
                        ab['Reason'].append('Invalid amount')
                        validation = False
                        av_ab = False
                        break
                if av_ab:
                    q = {'Reason': ['Invalid amount']}
                    q_a = counter.add_item(i, q)
                    database.invalid_data.append(q_a)
                    validation = False
                
            if validation:
                database.valid_data.append(i)



        # print(json.dumps(database.valid_data, indent=4))
        # print(database.valid_data)
        # print(database.invalid_data)
        # print(database.duplicate_data)
        # print(database.unique_emails)

    print(
        f'{'='*10} Summary {'='*10}\n\n'
        f'{'Total Leads':<20}: {database.total_leads}\n'
        f'{'Invalid Leads':<20}: {len(database.invalid_data)}\n'
        f'{'Valid Leads':<20}: {len(database.valid_data)}\n'
        f'{'Duplicate Leads':<20}: {len(counter.duplicate_counter(database.duplicate_data))}\n\n'
        f'Valid Leads:\n'
    )
    for i in database.valid_data:
        for x, y in i.items():
            print(f'{x} : {y}')
        print('\n')

    print('Invalid leads:\n')
    for i in database.invalid_data:
        for x, y in i.items():
            print(f'{x} : {y}')
        print('\n')

    print('Duplicate Leads:\n')
    for i in database.duplicate_data:
        for x, y in i.items():
            print(f'{x} : {y}')
        print(f'\n')


    header = ['lead_id','name','email','phone','country','amount']
    with open("Clean_leads.csv", 'w', encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames = header
        )

        writer.writeheader()
        writer.writerows(database.valid_data)


    
    header_inv = ['lead_id','name','email','phone','country','amount', 'Reason']
    with open('Invalid_leads.csv', 'w', encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames= header_inv
        )
        writer.writeheader()
        for i in database.invalid_data:
            writer.writerow(i)

    header_dup = ['lead_id','name','email','phone','country','amount', 'Duplicate by']
    with open('Duplicate_leads.csv', 'w', encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames = header_dup
        )

        writer.writeheader()

        for i in database.duplicate_data:
            writer.writerow(i)


except FileNotFoundError:
    print('File not Found')

except OSError:
    print('Use appropriate Operating System')
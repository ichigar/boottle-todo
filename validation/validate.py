class Validate:
    def __init__(self, data, rules):
        self.data = data
        self.rules = rules
        self.errors = {}
        return self.validate()
        
    def validate(self):
        for field, rule in self.rules.items():
            if rule == 'not_empty':
                self.validate_not_empty(field)
            # elif rule == 'is_number':
            #     self.validate_is_number(field)
            # elif rule == 'is_email':
            #     self.validate_is_email(field)
            # elif rule == 'is_url':
            #     self.validate_is_url(field)
            # elif rule == 'is_ip':
            #     self.validate_is_ip(field)
            # elif rule == 'is_date':
            #     self.validate_is_date(field)
            # elif rule == 'is_datetime':
            #     self.validate_is_datetime(field)
            # elif rule == 'is_time':
            #     self.validate_is_time(field)
            # elif rule == 'is_bool':
            #     self.validate_is_bool(field)
            # elif rule == 'is_list':
            #     self.validate_is_list(field)
            # elif rule == 'is_list_of_numbers':
            #     self.validate_is_list_of_numbers(field)
            # elif rule == 'is_list_of_emails':
            #     self.validate_is_list_of_emails(field)
            # elif rule == 'is_list_of_urls':
            #     self.validate_is_list_of_urls(field)
            # elif rule == 'is_list_of_ips':
            #     self.validate_is_list_of_ips(field)
            # elif rule == 'is_list_of_dates':
            #     self.validate_is_list_of_dates(field)
            # elif rule == 'is_list_of_datetimes':
            #     self.validate_is_list_of_datetimes(field)
            # elif rule == 'is_list_of_times':
            #     self.validate_is_list_of_times(field)
            # elif rule == 'is_list_of_bools':    
            #     self.validate_is_list_of_bools(field)
        return self.errors
    def validate_not_empty(self, field):
        if not self.data[field]:
            self.errors[field] = 'This field is required'

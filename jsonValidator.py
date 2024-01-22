import json
from itertools import chain

class jsonValidator:
    def validate_schema(self, 
        json_file:str, 
        schema_file:str
        ) -> bool:
        
        #gathering the contents of json file
        with open(json_file, 'r') as content:
            data = json.load(content)
        
        #gathering the contents of schema file
        with open(schema_file, 'r') as check:
            schema = json.load(check)


        #gathering all the information about the fields from schema file
        
        required_fields = schema.get("required")

        #using chain to flatten list because if the "anyOf" block in schema file contains multiple required keyword then it will become list of lists.
        at_least_one_fields = list(chain.from_iterable([item["required"] for item in schema.get("anyOf")]))
        either_fields = list(chain.from_iterable([item["required"] for item in schema.get("oneOf")]))
        
        mutually_exclusive_fields = schema.get("not")["required"]
        enum_fields = [(field, schema["properties"][field].get("enum")) for field in schema.get("properties") if schema["properties"][field].get("enum")]

        #checking whether the data file satisfies the conditions in the schema or not
        data_fields = list(data.keys()) #

        #checking all mandatory fields present or not
        required = all(field in data_fields for field in required_fields)


        #checking whether the one of the fields among required fields present or not
        at_least = any(field in data_fields for field in at_least_one_fields)
        
        #checking either one of two required fields are present or not
        either = any(field in data_fields for field in either_fields)
    
        # checking which of mutually exclusive fields 
        not_both_check = [field in data_fields for field in mutually_exclusive_fields]    
        not_both = any(not_both_check) and not all(not_both_check) # this is XOR operation which means all fields cannot be true (or false).
        
        #checking whether the field like "day" which supports enum values are present or not
        one_of_present = [field[0] in data_fields for field in enum_fields]

        #first condition checks that all the conditions above are satisfied
        if required and at_least and either and not_both:
            #this block of code checks whether the value of the fields with enum values are from allowed values or not
            if any(one_of_present):
                is_ok = [] # if there are multiple fields with enum values
                for field, allowed in enum_fields:
                    is_ok.append(data[field] in allowed)
                return all(is_ok) # returns true after the value of each field is true from its corresponding allowed values
            
            return True # returns true if all conditions are satisfied and there is no enum field present

        return False #else false (i.e, one of the condition is violated)
    

validate  = jsonValidator()

isCorrect = validate.validate_schema('sample.json', 'schema.json')
#change sample to valid or invalid_sample, you can test other JSON file also.

#Assuming that the given task needs to done without using any library, otherwise this can also be done usinf the jsonschema library.

print(isCorrect)

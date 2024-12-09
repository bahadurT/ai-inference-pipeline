"""
********************************************
*                                          *
*           Author: Bahadur Singh Thakur
*           E-mail: bahadur.th7@gmail.com  *
*           Date: 12-Dec-2024              *
*                                          *
********************************************
"""
import json

class Rules:
    def __init__(self, name, details):
        self.name = name
        self.details = details

class CameraRule:
    def __init__(self, rule_list):
        self.rule_names = []
        self.rule_categories = {}
        self.rule_details = {}
        self.rule_list = self._parse_rules(rule_list)

    def _parse_rules(self, rule_list):
        rules = []
        for rule in rule_list:
            for rule_name, rule_data in rule.items():
                self.rule_names.append(rule_name)
                self.rule_categories[rule_name] = []
                self.rule_details[rule_name] = {}
                for rule_category_list in rule_data:
                    for rule_category, rule_details_list in rule_category_list.items():
                        self.rule_categories[rule_name].append(rule_category)
                        if rule_category not in self.rule_details[rule_name]:
                            self.rule_details[rule_name][rule_category] = []
                        for rule_details in rule_details_list:
                            self.rule_details[rule_name][rule_category].append(rule_details)
                            for category_name, category_details in rule_details.items():
                                rules.append(Rules(f"{rule_name}::{rule_category}::{category_name}", category_details))
        return rules

def load_rules_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    camera_rules = {}
    for camera_id, camera_data in data.items():
        for config in camera_data:
            rule_list = config.get("rule_list", [])
            camera_rule = CameraRule(rule_list)
            camera_rules[camera_id] = camera_rule
    return camera_rules

def main():
    json_file = 'rules.json'
    camera_rules = load_rules_from_json(json_file)
    camera_rule = camera_rules['camera1']
    for x in camera_rule.rule_details.items():
        print(x)
    '''for camera_id, camera_rule in camera_rules.items():
        print(f"Camera ID: {camera_id}")
        for rule_name, categories in camera_rule.rule_details.items():
            print(f"  Rule Name: {rule_name}")
            for category, details_list in categories.items():
                print(f"    Category: {category}")
                for details in details_list:
                    for key, value in details.items():
                        print(f"      {key}: {value}")'''

if __name__ == "__main__":
    main()


from collections import OrderedDict
import json
import pandas as pd

xlsx_path = './티에프이_키워드.xlsx'
df = pd.read_excel(xlsx_path, engine='openpyxl')

test_dict = {}
test_dict = df.to_dict()

print(test_dict)

json_test = df.to_json(force_ascii=False)
print(json_test)

with open('./티에프이_키워드.json', 'w', encoding="utf-8") as make_file:
    json.dump(json_test, make_file, ensure_ascii=False, indent=None)
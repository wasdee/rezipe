import pint

mother_of_units = pint.UnitRegistry()

# https://github.com/hgrecco/pint/blob/master/pint/default_en.txt
ถ้วย = cup = mother_of_units.cup
ช้อนชา = ชช = tsp = teaspoon = mother_of_units.teaspoon
ช้อนโต๊ะ = ชต = tbsp = tablespoon = mother_of_units.tablespoon

gram = กรัม = mother_of_units.gram

cal = แคล = แคลอรี่ = mother_of_units.calorie

min_ = นาที = mother_of_units.minute
hr = hour = ชั่วโมง = mother_of_units.hour
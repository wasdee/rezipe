"""
Wongnai Aroi Sat: 

อร่อยศาสตร์ Season 2 EP. 6 : ทอดไข่เจียวอย่างไร ให้ได้ไข่ที่ฟูนุ่มน่ากิน
https://www.youtube.com/watch?v=eeIpZX0kcEc
"""

egg_part = ตีไข่([Egg(size=0,temp=Temp.room)*2, Milk(volume=1 TableSpoon)], times=50)

pot = heat(cyclidical_pot.add(DeepFriendOil(mL=175)), until=DeepFriendOil(temp=180))

pot = pour(egg_part, pot, height_from_table=BodyHeight.shoulder)

if smell() == 'nice':
    pot.content.flip()

if judgement() == 'done':
    pot.content.serve()
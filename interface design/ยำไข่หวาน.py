"""
metaflow inspired api
"""

# class >< เมนู

kcal = serving = 1 

from rezipe import Recipe, step

class ยำไข่หวาน(Recipe):

    meta = {
        'เวลาเตรียม': 10 * min,
        'เวลาปรุง': 25 * min,
        'แคลลอรี่': 500 *kcal/serving,
        'สำหรับ': 10 * serving
    }

    @step
    def ต้มไข่(self, ไข่เป็ด=10, เกลือ=1, น้ำส้มสายชู=1):
        """
        
        """
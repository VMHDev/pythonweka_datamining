# Khai báo class
class ItemAP():
    # Khai báo các thuộc tính:
    ItemSet = []
    Support = 0
    SupportCount = 0

    # Phương thức khởi tạo
    def __init__(self, _ItemSet = [], _Support = 0, _SupportCount = 0):
        self.ItemSet = _ItemSet
        self.Support = _Support
        self.SupportCount = _SupportCount

    # Phương thức xuất dữ liệu
    def ToString(self):
        return str(round(self.Support, 2)) + ' ' + ', '.join(self.ItemSet)

##########################################################################################################################################################
# Test hàm kiểm tra có tổ hợp được
def IsValidCombine(_ItemFirst, _ItemSecond, _Step):
    for i in range(_Step):
        if(_ItemFirst.ItemSet[i] != _ItemSecond.ItemSet[i]):
            return False
    return True

item1 = 'Bread'
item3 = 'Milk'
objItemAP1 = ItemAP([], 0, 0)
objItemAP1.ItemSet.append(item1)
objItemAP1.ItemSet.append(item3)

item2 = 'Bread'
item4 = 'Cheese'
objItemAP2 = ItemAP([], 0, 0)
objItemAP2.ItemSet.append(item2)
objItemAP2.ItemSet.append(item4)

rs = IsValidCombine(objItemAP1, objItemAP2, 1)
print(rs)
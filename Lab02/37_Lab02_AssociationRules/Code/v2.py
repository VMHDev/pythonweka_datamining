from sys import argv
import csv

##########################################################################################################################################################
##########################################################################################################################################################
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
##########################################################################################################################################################
# Hàm đọc file dữ liệu:
def ReadFileCSV(_PathInput, _NameItem):
    # Đảm bảo là file .csv
    extension = '.csv'
    if extension not in _PathInput:
        _PathInput += extension
    
    with open(_PathInput) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        dataAP = list(csv_reader)

    # Lấy tên các item
    for name in dataAP[0]:
        _NameItem.append(name)

    # Xóa header - Trả về tập dữ liệu không header
    del dataAP[0]
    return dataAP

# Hàm ghi file tập phổ biến
def WriteFileFI(_PathOutputFI, _DataFreq):
    f2 = open(_PathOutputFI, 'w+')
    for item in _DataFreq:
        if item == _DataFreq[-1]:
            f2.write(item.ToString())
        else:
            f2.write(item.ToString() + '\n')

# Hàm phát sinh tập ứng viên C1
def GenCandicate(_DataHeader, _DataAP):
    # Lấy danh sách tên các item
    lstItemCand = []
    for item in _DataHeader:
        objItemAP = ItemAP([], 0, 0)
        objItemAP.ItemSet.append(item)
        lstItemCand.append(objItemAP)

    # Xác định Support Count (Đếm hỗ trợ) của các item
    for itemTrans in _DataAP:
        for index, item in enumerate(itemTrans):
            if(item == 'y'):
                lstItemCand[index].SupportCount += 1

    return lstItemCand


 # Hàm phát sinh tập phổ biến F1

# Hàm phát sinh tập phổ biến F1
def GenFrequentItemset(_DataCand, _MinSupp, _DataSize):
    lstFreItem = []
    # Xác định item thỏa minsupp để đưa vào F
    for itemCand in _DataCand:
        itemCand.Support = itemCand.SupportCount/_DataSize
        if(itemCand.Support >= _MinSupp):
            lstFreItem.append(itemCand)
    return lstFreItem
    
#-----------------------------------------------------------------------------------------------------------------------------------
def main(argv):
    lstNameItem = []
    dataAP = ReadFileCSV('input01.csv', lstNameItem)

    dataCand = GenCandicate(lstNameItem, dataAP)
    dataFreq = GenFrequentItemset(dataCand, 0.3, len(dataAP))
    WriteFileFI('FI.txt', dataFreq)


if __name__ == "__main__":
    main(argv)
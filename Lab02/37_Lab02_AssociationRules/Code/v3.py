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
def GenFrequentItemset(_DataCand, _MinSupp, _DataSize):
    lstFreItem = []
    # Xác định item thỏa minsupp để đưa vào F
    for itemCand in _DataCand:
        itemCand.Support = itemCand.SupportCount/_DataSize
        if(itemCand.Support >= _MinSupp):
            lstFreItem.append(itemCand)
    return lstFreItem

#-------------------------------------------------------------------------------------------------------------------------------------
# Hàm kiểm tra tổ hợp item có hợp lệ
def IsValidCombine(_ItemFirst, _ItemSecond, _Step):
    for i in range(_Step):
        if(_ItemFirst.ItemSet[i] != _ItemSecond.ItemSet[i]):
            return False
    return True

# Tạo danh sách các giao dịch từ dữ liệu đầu vào
# _DataAP: Dữ liệu dạng 'y' - 'n'
# _NameItem: Tên của các item
def CreateListTransactionFromInput(_DataAP, _NameItem):
    lstTrans = []
    trans = []
    for itemTrans in _DataAP:
        for index, item in enumerate(itemTrans):
            if(item == 'y'):
                trans.append(_NameItem[index])
        lstTrans.append(trans.copy())
        trans.clear()
    return lstTrans

# Lấy đếm độ trợ - support count của các item
# _LstTrans: Danh sách các giao dịch
# _ItemAP: Item cần lấy support count
def GetSuppportCountItem(_LstTrans, _ItemAP):
    iSupp = 0
    for trans in _LstTrans:
        check = True
        for i in range(len(_ItemAP.ItemSet)):
            if(_ItemAP.ItemSet[i] not in trans):
                check = False
                break
        if(check):
            iSupp += 1
    return iSupp

# Hàm phát sinh tập ứng viên Ck
def GenCandicate_K(_DataF1, _DataAP, _NameItem):
    # Lấy danh sách tên các item
    lstItemCand = []
    for i in range(len(_DataF1)):
        for j  in range(i + 1, len(_DataF1)):
            if(IsValidCombine(_DataF1[i], _DataF1[j], 0)):
                objItemAP = ItemAP([], 0, 0)
                itemCombine = []
                itemCombine = _DataF1[i].ItemSet.copy()
                itemCombine.append(_DataF1[j].ItemSet[-1])
                objItemAP.ItemSet = itemCombine.copy()
                lstItemCand.append(objItemAP)        

    #Xác định Support Count (Đếm hỗ trợ) của các item
    lstTrans = CreateListTransactionFromInput(_DataAP, _NameItem)
    for item in lstItemCand:
        item.SupportCount = GetSuppportCountItem(lstTrans, item)
    return lstItemCand

 # Hàm phát sinh tập phổ biến Fk

# Hàm phát sinh tập phổ biến Fk
def GenFrequentItemset_K(_DataCandF1, _MinSupp, _DataSize):
    lstFreItem = []
    # Xác định item thỏa minsupp để đưa vào F
    for itemCand in _DataCandF1:
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
    

    dataCand2 = GenCandicate_K(dataFreq, dataAP, lstNameItem)
    dataFreq2 = GenFrequentItemset_K(dataCand2, 0.3, len(dataAP))

    datars = dataFreq.copy()
    datars.extend(dataFreq2)
    WriteFileFI('FI.txt', datars)
    
    # Test CreateListTransactionFromInput và GetSuppportCountItem
    # lstTrans = CreateListTransactionFromInput(dataAP, lstNameItem)
    # objItemAP = ItemAP([], 0, 0)
    # objItemAP.ItemSet.append('Beef')
    # objItemAP.ItemSet.append('Cheese')
    # GetSuppportCountItem(lstTrans, objItemAP)

if __name__ == "__main__":
    main(argv)
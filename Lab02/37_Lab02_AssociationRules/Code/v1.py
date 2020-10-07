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
        print (str(round(self.Support, 2)) + ' ' + ', '.join(self.ItemSet))

##########################################################################################################################################################
##########################################################################################################################################################
# Hàm đọc file dữ liệu:
def ReadFileCSV(_PathInput):
    # Đảm bảo là file .csv
    extension = '.csv'
    if extension not in _PathInput:
        _PathInput += extension
    
    with open(_PathInput) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = list(csv_reader)
    #header = ReadFileCSV(data[0])
    #del data[0]  # remove header

    return data

def ReadFileCSV2(_PathInput, _NameItem):
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

# Hàm ghi file 
def WriteFileFI(_PathOutputFI, _DataFreq):
    f2 = open(_PathOutputFI, 'w+')
    for item in _DataFreq:
        item.ToString()
    

# Hàm phát sinh tập ứng viên C
def GenCandicate(_DataHeader, _DataAP):
    # Lấy danh sách tên các item
    lstItemSet = []
    for item in _DataHeader:
        objItemAP = ItemAP([], 0, 0)
        objItemAP.ItemSet.append(item)
        lstItemSet.append(objItemAP)

    # Xác định Support Count (Đếm hỗ trợ) của các item
    for itemTrans in _DataAP:
        for index, item in enumerate(itemTrans):
            if(item == 'y'):
                lstItemSet[index].SupportCount += 1

    # lstCand = []
    # lstCand.append(lstItemSet)
    return lstItemSet


 # Hàm phát sinh tập phổ biến F
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
    # Lấy thông tin các tham số
    # pathInput = argv[1]             # Đường dẫn file input dữ liệu khảo sát
    # pathOutputFI = argv[2]          # Đường dẫn file output danh sách tập hạng mục phổ biến
    # pathOutputAR = argv[3]          # Đường dẫn file output danh sách các luật kết hợp
    # sMinSupp = argv[4]              # Giá trị độ phổ biến tối thiểu
    # sMinConf = argv[5]              # Giá trị độ tin cậy tối thiểu

    # Xử lý các tham số
    # iMinSupp = int(sMinSupp)
    # iMinConf = int(sMinConf)

    # print(pathInput)
    # print(pathOutputFI)
    # print(pathOutputAR)
    # print(iMinSupp)
    # print(iMinConf)

    # Đọc file input:
    #data = ReadFileCSV('input01.csv')
    # for item in data:
    #     for itemChild in item:
    #         print(itemChild)

    lstNameItem = []
    dataAP = ReadFileCSV2('input01.csv', lstNameItem)
    # for item in data:
    #     print(item)
    #     for itemChild in item:
    #         print(itemChild)
    # print(lstNameItem)
    #print(len(dataAP))

    dataCand = GenCandicate(lstNameItem, dataAP)
    dataFreq = GenFrequentItemset(dataCand, 0.3, len(dataAP))
    #WriteFileFI('FI.txt', '')


if __name__ == "__main__":
    main(argv)
from sys import argv
from itertools import groupby
import math
import csv
##########################################################################################################################################################
##########################################################################################################################################################
# Khai báo class
class AtrributeData():
    # Khai báo các thuộc tính:
    Value = []
    Size = 0

    # Phương thức khởi tạo
    def __init__(self, _Value = [], _Size = 0):
        self.Value = _Value
        self.Size = _Size

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
class ItemFrequency():
    # Khai báo các thuộc tính:
    AttributeValue = ''             # Giá trị thuộc tính
    Frequency = 0                   # Số lần xuất hiện

    # Phương thức khởi tạo
    def __init__(self, _AttributeValue = '', _Frequency = 0):
        self.AttributeValue = _AttributeValue
        self.Frequency = _Frequency
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
class ItemEntropy():
    # Khai báo các thuộc tính:
    AttributeValue = ''             # Giá trị thuộc tính
    Entropy = 0                     # Độ đo Entropy

    # Phương thức khởi tạo
    def __init__(self, _AttributeValue = '', _Entropy = 0):
        self.AttributeValue = _AttributeValue
        self.Entropy = _Entropy

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
class ItemAE():
    # Khai báo các thuộc tính:
    AttributeValue = ''             # Giá trị thuộc tính
    AE = 0                          # Độ đo Entropy trung bình

    # Phương thức khởi tạo
    def __init__(self, _AttributeValue = '', _AE = 0):
        self.AttributeValue = _AttributeValue
        self.AE = _AE
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
class ItemID3():
    # Khai báo các thuộc tính:
    ItemSet = []
    Support = 0
    SupportCount = 0

    AtrrName = ''
    Entropy = 0

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
    dataInput = []
    try:
        # Đảm bảo là file .csv
        extension = '.csv'
        if extension not in _PathInput:
            _PathInput += extension

        with open(_PathInput) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            dataInput = list(csv_reader)

        # Lấy tên các item
        for name in dataInput[0]:
            _NameItem.append(name)

        # Xóa header - Trả về tập dữ liệu không header
        del dataInput[0]
    except:
      print("Không tìm thấy file hoặc file không hợp lệ!")
    return dataInput

# Hàm tính Entropy"
def CalcEntropy(_NumPos, _NumNeg, _NumValue):
    if(_NumPos == 0):
        return (-_NumNeg/_NumValue)*math.log(_NumNeg/_NumValue,2)
    elif (_NumNeg == 0):
        return (-_NumPos/_NumValue)*math.log(_NumPos/_NumValue,2)
    elif (_NumValue == 0):
        return 0
    else:
        return (-_NumPos/_NumValue)*math.log(_NumPos/_NumValue,2) + (-_NumNeg/_NumValue)*math.log(_NumNeg/_NumValue,2)
    

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
# Hàm khởi tạo thuật toán ID3:
def InitID3(_Data, _LstNameAtrr, _InfoAttributeClassify):
    lstAE = []
    for idxCol in range(0, len(_Data[0]) - 1, 1):
        lstValueAttr = []       # Danh sách giá trị các thuộc tính
        lstValueAttrPos = []    # Danh sách giá trị các thuộc tính theo phân lớp dương Pos (là giá trị đầu tiên trong phân lớp)
        lstValueAttrNeg = []    # Danh sách giá trị các thuộc tính theo phân lớp âm Neg (là giá trị thứ hai trong phân lớp)
        iCountItem = 0;         # Số lượng giá trị các thuộc tính
        iCountItemPos = 0;      # Số lượng giá trị các thuộc tính theo phân lớp dương Pos
        iCountItemNeg = 0       # Số lượng giá trị các thuộc tính theo phân lớp âm Neg

        #----------------------------------------------------------------------
        # Đếm số lượng giá trị các thuộc tính theo thuộc tính phân lớp
        for idxRow, itemAtrrCount in enumerate(_Data):
            # Đếm tất cả
            lstValueAttr.append(itemAtrrCount[idxCol])
            iCountItem += 1
            # Đếm theo thuộc tính dương
            if(itemAtrrCount[-1] == _InfoAttributeClassify.Value[0]):
                lstValueAttrPos.append(itemAtrrCount[idxCol])
                iCountItemPos += 1
            # Đếm theo thuộc tính âm
            if(itemAtrrCount[-1] == _InfoAttributeClassify.Value[1]):
                lstValueAttrNeg.append(itemAtrrCount[idxCol])
                iCountItemNeg += 1    

        #----------------------------------------------------------------------
        # Nhóm các thuộc - Tính số lần xuất hiện
        lstValueAttrGrp = []
        for value, freq in groupby(sorted(lstValueAttr)):
            itemAtrrFreq = ItemFrequency([], 0) 
            itemAtrrFreq.AttributeValue = value
            itemAtrrFreq.Frequency = len(list(freq))
            lstValueAttrGrp.append(itemAtrrFreq)

        lstValueAttrPosGrp = []
        for value, freq in groupby(sorted(lstValueAttrPos)):
            itemAtrrFreqPos = ItemFrequency([], 0) 
            itemAtrrFreqPos.AttributeValue = value
            itemAtrrFreqPos.Frequency = len(list(freq))
            lstValueAttrPosGrp.append(itemAtrrFreqPos)

        lstValueAttrNegGrp = []
        for value, freq in groupby(sorted(lstValueAttrNeg)):
            itemAtrrFreqNeg = ItemFrequency([], 0) 
            itemAtrrFreqNeg.AttributeValue = value
            itemAtrrFreqNeg.Frequency = len(list(freq))
            lstValueAttrNegGrp.append(itemAtrrFreqNeg)

        #----------------------------------------------------------------------
        # Tính các Entropy
        lstEntropy = []
        for itemAtrrEntropy in lstValueAttrGrp:
            objPos = ItemFrequency([], 0) 
            objNeg = ItemFrequency([], 0)
            objItemEntropy = ItemEntropy('', 0)

            # Lấy thông item Pos có cùng giá trị với itemAtrr đang xét
            for itemPos in lstValueAttrPosGrp:
                if(itemPos.AttributeValue == itemAtrrEntropy.AttributeValue):
                    objPos.AttributeValue = itemPos.AttributeValue
                    objPos.Frequency = itemPos.Frequency
                    break

            # Lấy thông item Neg có cùng giá trị với itemAtrr đang xét
            for itemNeg in lstValueAttrNegGrp:
                if(itemNeg.AttributeValue == itemAtrrEntropy.AttributeValue):
                    objNeg.AttributeValue = itemNeg.AttributeValue
                    objNeg.Frequency = itemNeg.Frequency
                    break

            # Tính Entropy các item
            objItemEntropy.AttributeValue = itemAtrrEntropy.AttributeValue
            objItemEntropy.Entropy = CalcEntropy(objPos.Frequency, objNeg.Frequency, itemAtrrEntropy.Frequency)
            lstEntropy.append(objItemEntropy)
        #----------------------------------------------------------------------

        # Tính entropy trung bình
        dAE = 0
        objAE = ItemAE('', 0)

        for itemEntropy in lstEntropy:
            for itemSumValue in lstValueAttrGrp:
                if(itemEntropy.AttributeValue == itemSumValue.AttributeValue):
                    dAE += (itemSumValue.Frequency/iCountItem) * itemEntropy.Entropy
                    break
        #----------------------------------------------------------------------
        objAE.AttributeValue = _LstNameAtrr[idxCol]
        objAE.AE = dAE
        lstAE.append(objAE)
    #----------------------------------------------------------------------
    return lstAE


# Hàm lấy thông tin của thuộc tính phân lớp:
def GetInfoAttributeClassify(_Data):
    objAtrributeData = AtrributeData([], 0)
    rowFirst = _Data[0]
    objAtrributeData.Value.append(rowFirst[-1])
    objAtrributeData.Size += 1
    for rowX in _Data:
        if(objAtrributeData.Value[0] != rowX[-1]):
            objAtrributeData.Value.append(rowX[-1])
            objAtrributeData.Size += 1
            break
    return objAtrributeData

##########################################################################################################################################################
##########################################################################################################################################################
def main(argv):
    # Lấy thông tin các tham số
    pathInput = argv[1]             # Đường dẫn file input dữ liệu khảo sát
    pathOutput = argv[2]          # Đường dẫn file output danh sách tập hạng mục phổ biến
    folds = argv[3]              # Giá trị độ phổ biến tối thiểu
    best_att = argv[4]              # Giá trị độ tin cậy tối thiểu
    
    # pathInput = 'input_play.csv'
    # pathOutput = 'model.txt'
    # folds = 10
    # best_att = 0

    lstNameAtrr = []
    dataInput = ReadFileCSV(pathInput, lstNameAtrr)
    if(len(dataInput) == 0):
        return
        
    objInfoAttributeClassify = GetInfoAttributeClassify(dataInput)
    ################################################################################################################################
    # Chọn thuộc tính lần 1
    print('----------------------- PHÂN LỚP ID3 -----------------------')
    print('------------------ Chọn thuộc tính lần 1 -------------------')
    print('- Tính Entropy trung bình: ')
    rs = InitID3(dataInput, lstNameAtrr, objInfoAttributeClassify)
    for item in rs:
        print(item.AttributeValue + ": AE = " + str(round(item.AE,3)))

if __name__ == "__main__":
    main(argv)

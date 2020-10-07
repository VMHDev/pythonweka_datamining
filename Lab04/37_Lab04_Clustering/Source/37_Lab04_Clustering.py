from sys import argv
from scipy.io import arff

# ##########################################################################################################################################################
# ##########################################################################################################################################################
# # Hàm đọc file dữ liệu:
def ReadFileARFF(_PathInput, _NameItem):
    dataInput = []
    try:
        # Đảm bảo là file .csv
        extension = '.arff'
        if extension not in _PathInput:
            _PathInput += extension

        data, meta = arff.loadarff(_PathInput)
        dataInput = data
        _NameItem = meta
    except:
      print("Không tìm thấy file hoặc file không hợp lệ!")
    return dataInput

# ##########################################################################################################################################################
# ##########################################################################################################################################################
def main(argv):
    #Lấy thông tin các tham số
    pathInput = argv[1]               # Đường dẫn file input dữ liệu khảo sát
    pathOutput = argv[2]              # Đường dẫn file output dữ liệu gom cụm
    k = argv[3]                       # Số cụm gom nhóm
    
    # pathInput = 'cardiology-cleaned.arff'
    # k = 2
    # pathOutput = str(k) + '-clusters.txt'

    # Đọc dữ liệu từ file arff
    dataInput = []
    try:
        extension = '.arff'
        if extension not in pathInput:
            _PathInput += extension

        data, meta = arff.loadarff(pathInput)
        dataInput = data
        lstNameAtrr = meta
    except:
      print("Không tìm thấy file hoặc file không hợp lệ!")

    if(len(dataInput) == 0):
        return

    print("Đọc dữ liệu từ file arff")
    nameAtrr = lstNameAtrr.names()
    print()
    print("Lấy tên thuộc tính:")   
    for name in nameAtrr:
        if(name != nameAtrr[-1]):
            print(name + ', ', end = '')
        else:
            print(name)
    print()
    print("Lấy dữ liệu:")  
    for item in data:
        print(item)
    ################################################################################################################################

    f2 = open(pathOutput, 'w+')
if __name__ == "__main__":
    main(argv)

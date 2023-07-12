import time

class Class:
    def __init__(self):
        self.nSlot = 0
        self.teacher = 0
        self.nStudents = 0
        self.choosenSlot = 0
        self.choosenRoom = 0
    
    def input(self, *value):
        self.nSlot, self.teacher, self.nStudents = map(int, values)


def Assignment(M, nTeacher, sorted_class, sorted_rooms ):

    usingTeacher = [[False] * 60 for _ in range(nTeacher + 1)]
    usingRoom = [[False] * 60 for _ in range(M)]

    # Xác định ngày, tiết và phòng cho mỗi lớp
    for chooseRoom in sorted_rooms:
        for idClass in sorted_class:
            for startSlot in range(1, 61):
                if capacity[chooseRoom] < classList[idClass].nStudents:
                    continue
            
                endSlot = startSlot + classList[idClass].nSlot - 1
                if (startSlot - 1) // 6 != (endSlot - 1) // 6:
                    continue
            
                checkValidArrangement = True
                for j in range(startSlot, endSlot + 1):
                    try:
                        if usingTeacher[classList[idClass].teacher][j]:
                            checkValidArrangement = False
                            break
                    except:
                        pass
                    
                    try:
                        if usingRoom[chooseRoom][j]:
                            checkValidArrangement = False
                            break
                    except:
                        pass

                if checkValidArrangement:
                    for j in range(startSlot, endSlot + 1):
                        try:
                            usingTeacher[classList[idClass].teacher][j] = True
                            usingRoom[chooseRoom][j] = True
                        except:
                            pass
                
                    classList[idClass].choosenSlot = startSlot
                    classList[idClass].choosenRoom = chooseRoom + 1
                    sorted_class = [c for c in sorted_class if c != idClass]
                    break
            

# Mở file và đọc input
with open("data.txt", "r") as file:
    # Đọc N và M từ file
    N, M = map(int, file.readline().split())

    # Tạo danh sách lớp
    classList = [Class() for _ in range(N)]

    # Đọc thông tin lớp từ file
    for i in range(N):
        values = map(int, file.readline().split())
        classList[i].input(values)

    # Đọc thông tin capacity từ file
    capacity = list(map(int, file.readline().split()))

# số lượng gv
nTeacher = max(classList, key=lambda x: x.teacher).teacher

t1 = time.time()

# sort theo so luong  sv
sorted_classes = sorted(range(N), key=lambda x: -classList[x].nStudents)

# sort theo suc chua
sorted_rooms = sorted(range(M), key=lambda x: -capacity[x])

Assignment(M, nTeacher, sorted_classes, sorted_rooms)

t2 = time.time()
# Assignment_sorted = sorted(classList, key=lambda x: x.choosenSlot)

maximum_Classes = 0
for index, assignment in enumerate(classList):
    if classList[index].choosenRoom and classList[index].choosenSlot:
        maximum_Classes += 1

print(maximum_Classes)

for index, assignment in enumerate(classList):
    if classList[index].choosenRoom and classList[index].choosenSlot:
        print(f"{index +1} {classList[index].choosenSlot} {classList[index].choosenRoom}")

print(f"Time solution: {t2-t1:.10f}")






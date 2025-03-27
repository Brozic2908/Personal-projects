import random           # Nhập thư viện random để sử dụng khi cần xáo trộn dữ liệu
import time             # Nhập thư viện time để sử dụng khi cần độ trễ hoặc đo thời gian
from tkinter import *   # Nhập tất cả các thành phần từ thư viện Tkinter để tạo giao diện đồ họa

root = Tk()                             # Tạo cửa sổ chính của ứng dụng
root.geometry("1100x650+0+0")           # Đặt kích thước cửa sổ là 1100x650 pixel và vị trí xuất hiện trên màn hình (0,0)
root.title("Puzzle game")               # Đặt tiêu đề của cửa sổ là "Puzzle game"
root.configure(background='Cadet Blue') # Thiết lập màu nền của cửa sổ là màu xanh Cadet Blue

# Tạo khung trên cùng (Tops) để chứa tiêu đề của trò chơi
Tops = Frame (
    root, 
    bg='Cadet Blue', # background color
    pady=2, # padding y
    width=1100,
    height=30, 
    relief=RIDGE
    #! Ngoài RIDGE, bạn có thể dùng các giá trị sau để thay đổi kiểu viền:
        # FLAT:     Không có viền.
        # SUNKEN:   Viền chìm xuống.
        # RAISED:   Viền nhô lên.
        # GROOVE:   Viền trông giống như một rãnh.
        # RIDGE:    Viền nổi dạng gờ (giống GROOVE nhưng ngược lại).
)  
Tops.grid(row=0, column=0)  # Đặt khung này vào hàng 0, cột 0 của lưới trong root

# Tạo nhãn tiêu đề và đặt vào trong khung Tops
lblTitle = Label(
    Tops,                           # Đặt nhãn này vào khung Tops
    font=('arial', 50, 'bold'),     # Thiết lập font chữ Arial, kích thước 80, in đậm
    text="Advanced Puzzle Game",    # Văn bản hiển thị trên nhãn
    bd=10,                          # Độ dày của viền
    bg='Cadet Blue',                # Màu nền của nhãn
    fg='Cornsilk',                  # Màu chữ là Cornsilk
    justify=CENTER                  # Căn giữa văn bản
)

lblTitle.grid(row=0, column=0)  # Đặt nhãn vào hàng 0, cột 0 của khung Tops

# Tạo khung chính (MainFrame) để chứa nội dung của trò chơi
MainFrame = Frame(root, bg='Powder Blue', bd=10, width=1040, height=600, relief=RIDGE)  
MainFrame .grid(row=1, column=0, padx=30)  # Đặt khung này vào hàng 1, cột 0 và thêm padding ngang 30px

# Tạo khung trái (leftFrame) để chứa trò chơi
leftFrame = Frame(MainFrame, bg='Cadet Blue', bd=10, width=600, height=450, pady=2, relief=RIDGE)  
leftFrame .pack(side=LEFT)

# Tạo khung Phải (rightFrame) để chứa số lượng click
rightFrame = Frame(MainFrame, bg='Cadet Blue', bd=10, width=430, height=450, padx=1, pady=2, relief=RIDGE)  
rightFrame .pack(side=RIGHT)

# Chia rightFrame thành 3 phần con (rightFrame1, rightFrame2, rightFrame3)
rightFrame1 = Frame(rightFrame, bg='Cadet Blue', bd=10, width=430, height=170, padx=10, pady=2, relief=RIDGE)  
rightFrame1 .grid(row=0, column=0)

rightFrame2 = Frame(rightFrame, bg='Cadet Blue', bd=10, width=430, height=130, padx=10, pady=2, relief=RIDGE)  
rightFrame2 .grid(row=1, column=0)

rightFrame3 = Frame(rightFrame, bg='Cadet Blue', bd=10, width=430, height=130, padx=10, pady=2, relief=RIDGE)  
rightFrame3 .grid(row=2, column=0)

# Biến đếm số lần click
numberOfClick = 0
displayClicks = StringVar()
displayClicks .set("Number of clicks" + "\n" + "0")

gameStateString = StringVar()

def upDateCounter():
    """Cập nhật số lần click trên giao diện"""
    global numberOfClick, displayClicks
    displayClicks .set("Number of clicks" + "\n" + str(numberOfClick))


def gameStateUpdate(gameState):
    """Cập nhật trạng thái trò chơi"""
    global gameStateString
    gameStateString.set(gameState)

class Button_:
    """Tạo nút với giá trị và vị trí trên giao diện"""
    def __init__(self, text_, x, y):    # khai báo để dùng các phương thức
        self.enterValue = text_         # Giá trị nút
        self.textTaken = StringVar()    
        self.textTaken.set(text_)       # Thiết lập giá trị ban đầu
        self.x = x                      # Giá trị x
        self.y = y                      # Giá trị y
        self.btnNumber = Button(
            leftFrame,
            textvariable = self.textTaken,
            font=('arial', 40),
            bd = 3,
            command= # command của một Button dùng để xác định hàm sẽ chạy khi nút được nhấn. 
            lambda i=self.x, j=self.y # lambda tạo một hàm tạm thời vì command chỉ nhập 1 hàm ẩn danh
            : emptySpotChecker(i, j)  # Gọi hàm kiểm tra vị trí trống
        )

        # Giải thích place()
        #     Trong Tkinter, có nhiều cách để bố trí widget (Button, Label, Frame, v.v.), bao gồm:
        #     ✅ .pack() Sắp xếp theo hàng dọc hoặc ngang.
        #     ✅ .grid() Sắp xếp theo dạng lưới (hàng, cột).
        #     ✅ .place() Định vị widget chính xác bằng tọa độ x, y.
        #     ⚡ Ở đây, .place() được dùng để đặt vị trí chính xác của nút trong giao diện.
        self.btnNumber.place(
            x = self.x*140,
            y = self.y*140,
            width = 140,
            height = 140
        )
# Function to mix numbers on buttons
def shuffle():
    global numberOfClick, displayClicks
    nums = [] # List of numbers from 1 to 11 and 1 blank cell

    for x in range(12): # Make a list of numbers from 1 to 11
        x += 1
        if x == 12:
            nums.append("") # A blank cell
        else:
            nums.append(str(x))
        
    # Shuffle the positions of the numbers
    for y in range(len(btnNumbers)): 
        for x in range(len(btnNumbers[y])):
            num = random.choice(nums)           # Get random number from list
            btnNumbers[y][x].textTaken.set(num) # Assign number to button
            nums.remove(num)                    # Remove the number
            
    numberOfClick = 0   # Reset number of clicks
    upDateCounter()     # Update display
    gameStateUpdate("") # Update game state

# Khung chứa nhãn hiển thị số lần click
lblDisplayClicks = Label(rightFrame, textvariable=displayClicks, font=('arial', 30), bg='Cadet Blue').place(x = 12, y = 12, width = 400, height = 140)
# Khung chứa nút new game
btnShuffle = Button(rightFrame2, text="New Game", font=('arial', 28), bg='Cadet Blue', bd = 5, command=shuffle).place(x = -6, y = 2, width = 400, height = 100)
# Khung chứa thông báo bạn đã chiến thắng
lblDisplayClicks = Label(rightFrame3, textvariable=gameStateString, font=('arial', 30), bg='Cadet Blue').place(x = -6, y = 2, width = 400, height = 100)

btnNumbers = [] # Tạo danh sách 2D chứa các đối tượng button_
name = 0        # Biến đếm số thứ tự cho nút

for y in range(3):
    btnNumbers_ = []                                    # Danh sách tạm thời cho từng hàng
    for x in range (4): 
        name += 1
        if name == 12:                                  # Nếu là ô cuối cùng thì đặt giá trị rỗng
            name = ""
        btnNumbers_.append(Button_(str(name), x, y))    # Tạo hàng các nút số để chơi
    btnNumbers.append(btnNumbers_)                      # Thêm hàng vào danh sách chính

# Tự động trộn các nút khi bắt đầu trò chơi
shuffle()

# Kiểm tra và di chuyển ô trống
def emptySpotChecker(y, x):
    global btnNumbers, numberOfClick

    # Nếu ô không phải là ô trống
    if btnNumbers[x][y].textTaken.get() != "":
        # Kiểm tra ô bên trái và phải
        for i in range(-1,2):
            newX = x + i

            if not(newX < 0 or len(btnNumbers) - 1 < newX or i == 0):   
                # Nếu ô bên cạnh là ô trống
                if btnNumbers[newX][y].textTaken.get() == "":
                    text = btnNumbers[x][y].textTaken.get()
                    btnNumbers[x][y].textTaken.set(btnNumbers[newX][y].textTaken.get())
                    btnNumbers[newX][y].textTaken.set(text)
                    winCheck()
                    break
            
        for j in range(-1, 2):                 # Kiểm tra ô trên và dưới
            newY = y + j
            if not (newY < 0 or len(btnNumbers[0]) - 1 < newY or j == 0):  # Kiểm tra phạm vi hợp lệ
                if btnNumbers[x][newY].textTaken.get() == "":  # Nếu ô trên hoặc dưới là ô trống
                    text = btnNumbers[x][y].textTaken.get()    # Lấy giá trị hiện tại
                    btnNumbers[x][y].textTaken.set(btnNumbers[x][newY].textTaken.get())  # Đổi chỗ với ô trống
                    btnNumbers[x][newY].textTaken.set(text)    # Gán giá trị mới cho ô trống
                    winCheck()                                 # Kiểm tra xem người chơi đã thắng chưa
                    break
                    
        numberOfClick +=1
        upDateCounter()

# Hàm kiểm tra bạn đã thắng hay chưa
def winCheck():
    lost = False
    for y in range(len(btnNumbers)):
        for x in range(len(btnNumbers[y])):
            if btnNumbers[y][x].enterValue != btnNumbers[y][x].textTaken.get():
                lost = True
                break
    if not lost:
        gameStateUpdate("You are a Winner!")

root.mainloop()  # Chạy vòng lặp chính của Tkinter để giữ cửa sổ hiển thị

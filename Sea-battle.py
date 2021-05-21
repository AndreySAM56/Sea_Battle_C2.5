import os
import time
import math
import random

width = 6    #размеры морского поля, установленные по умолчанию
height = 6    # можно изменить в настройках соответсвенно измениться размер поля
level = 1   # уровень сложности игры, установленный по умолчанию
cell = " "  # Обозначение пустой ячейки на поле
ship = chr(9632) # обозначение корабля на поле
wounded = "V" # обозначение раненого корабля, т.е. попали но не убили
killed = "X" # обозначение убитого корабля
miss = "o" # обозначение промаха
around_ship = "~" # обозначение вокруг корабля (свободные границы)
ship_kol = [4,2,1,0,0,0,0,0]  # колличество кораблей, установленно по умолчанию, но можно изменить в настройках
                    # положение в списке, соответсвует количеству палуб. ship[0] - это однопалубный, ship[4] - пятипалубный
valid_characters = list(range(31)) # объявляю список длинной 31
valid_characters[0]=45   # список кодов допустимых символов
for i in range(10):     # заполняю этот список кодами цифр и кодами букв для проверки введённых координат
    valid_characters[i+1]=48+i
for i in range(20):
    valid_characters[11+i] = 65+i

# Классы

class SeaField: # класс морского поля
    def __init__(self,name,field1): # конструктор
        self.field = field1 # двумерный массив, игровое поле
        self.name = name
        self.list_ships = []
        self.victory = 0
    def fieldshow(self,show):  # метод который выводит поле на экран, show - ключ (True/False) показывать корабли или нет
        print("    ", end="")
        for horizontal in range(width):
            print(" | ", chr(65 + horizontal),sep="", end="")
        print(" |",end="")
        for vertical in range(height):
            print("")
            print("  --", end="")
            for horizontal in range(width):
                print("----", end="")
            print("--")
            if vertical<9:
                print("  ",vertical+1, end="")
            else: print(" ",vertical+1, end="")
            for horizontal in range(width):
                if (isinstance(self.field[vertical][horizontal],Ships) == True):
                    if show:
                        print(" | ", self.field[vertical][horizontal].name, sep="", end="")
                    else:
                        print(" | ", " ", sep="", end="")
                else:
                    print(" | ",self.field[vertical][horizontal],sep="", end="")
            print(" |", end="")
        print("")
        print("  --", end="")
        for horizontal in range(width):
            print("----", end="")
        print("--")
    def place_check(self, line, pillar, size): # метод проверяет, есть ли место на поле по указаным координатам и размерам
        line=line-1
        pillar=pillar-1
        l=abs(size)+1
        result=True
        if size>0:
            for i in range(l):
                try:
                    if self.field[line][pillar+i] != cell: result=False
                except IndexError:
                    result=False
                if line != 0:
                    try:
                        if isinstance(self.field[line-1][pillar+i],Ships): result=False
                    except IndexError:
                        pass
                try:
                    if isinstance(self.field[line + 1][pillar+i],Ships): result = False
                except IndexError:
                    pass
            for i in range(3):
                if (pillar != 0) and (line-1+i>=0):
                    try:
                        if isinstance(self.field[line-1+i][pillar-1],Ships): result = False
                    except IndexError:
                        pass
                if line-1+i>=0:
                    try:
                        if isinstance(self.field[line-1+i][pillar+abs(size)+1],Ships): result = False
                    except IndexError:
                        pass
        elif size<0:
            for i in range(l):
                try:
                    if self.field[line+i][pillar] != cell: result=False
                except IndexError:
                    result=False
                if pillar != 0:
                    try:
                        if isinstance(self.field[line+i][pillar-1],Ships): result=False
                    except IndexError:
                        pass
                try:
                    if isinstance(self.field[line+i][pillar+1],Ships): result = False
                except IndexError:
                    pass
            for i in range(3):
                if (line != 0) and (pillar-1+i>= 0):
                    try:
                        if isinstance(self.field[line-1][pillar-1+i],Ships): result = False
                    except IndexError:
                        pass
                if pillar-1+i>= 0:
                    try:
                        if isinstance(self.field[line+abs(size)+1][pillar-1+i],Ships): result = False
                    except IndexError:
                        pass
        elif size == 0:
            try:
                if self.field[line][pillar] != cell: result = False
            except IndexError:
                result = False
            for i in range(3):
                if (line!=0) and (pillar-1+i>= 0):
                    try:
                        if isinstance(self.field[line-1][pillar-1+i],Ships): result = False
                    except IndexError:
                        pass
                if pillar-1+i>= 0:
                    try:
                        if isinstance(self.field[line+1][pillar-1+i],Ships): result = False
                    except IndexError:
                        pass
            if pillar!=0:
                try:
                    if isinstance(self.field[line][pillar - 1],Ships): result = False
                except IndexError:
                    pass
            try:
                if isinstance(self.field[line][pillar + 1],Ships): result = False
            except IndexError:
                pass
        return result

    def installation_ships(self, line, pillar, size,ship): # метод который обозначет корабли на поле со свободной зоной
        line = line - 1
        pillar = pillar - 1
        l = abs(size) + 1
        if size > 0:
            for i in range(l):
                self.field[line][pillar + i] = ship
                if line!=0:
                    try:
                        if self.field[line - 1][pillar + i] == cell:
                            self.field[line - 1][pillar + i] = around_ship
                    except IndexError: pass
                try:
                    if self.field[line + 1][pillar + i] == cell:
                        self.field[line + 1][pillar + i] = around_ship
                except IndexError: pass
            for i in range(3):
                if (pillar != 0) and (line-1+i>=0):
                    try:
                        if self.field[line - 1 + i][pillar - 1] == cell:
                            self.field[line - 1 + i][pillar - 1] = around_ship
                    except IndexError: pass
                if line-1+i>=0:
                    try:
                        if self.field[line - 1 + i][pillar + abs(size) + 1] == cell:
                            self.field[line - 1 + i][pillar + abs(size) + 1] =around_ship
                    except IndexError: pass
        elif size < 0:
            for i in range(l):
                self.field[line+i][pillar] = ship
                if pillar!=0:
                    try:
                        if self.field[line + i][pillar - 1] == cell:
                            self.field[line + i][pillar - 1] = around_ship
                    except IndexError:
                        pass
                try:
                    if self.field[line + i][pillar + 1] == cell:
                        self.field[line + i][pillar + 1] = around_ship
                except IndexError:
                    pass
            for i in range(3):
                if (line != 0) and (pillar-1+i>=0):
                    try:
                        if self.field[line - 1][pillar - 1+i] ==cell:
                            self.field[line - 1][pillar - 1+i] = around_ship
                    except IndexError:
                        pass
                if pillar-1+i>=0:
                    try:
                        if self.field[line + abs(size) + 1][pillar - 1+i] == cell:
                            self.field[line + abs(size) + 1][pillar - 1+i] = around_ship
                    except IndexError:
                        pass
        elif size == 0:
            self.field[line][pillar] = ship
            for i in range(3):
                if (line != 0) and (pillar -1+i>= 0):
                    try:
                        if self.field[line - 1][pillar-1 + i] == cell:
                            self.field[line - 1][pillar-1 + i] = around_ship
                    except IndexError:
                        pass
                if pillar-1+i>=0:
                    try:
                        if self.field[line + 1][pillar-1 + i] ==cell:
                            self.field[line + 1][pillar-1 + i] = around_ship
                    except IndexError:
                        pass
            if pillar!=0:
                try:
                    if self.field[line][pillar - 1] ==cell:
                        self.field[line][pillar - 1] =around_ship
                except IndexError:
                    pass
            try:
                if self.field[line][pillar + 1] == cell:
                    self.field[line][pillar + 1] = around_ship
            except IndexError:
                pass
    def clearfield(self): # метод очистки игрового поля
        self.field=[]   # Обнуляем всё
        for i in range(height):
            self.field.append([" "]*width)

    def placement_ship(self,line,pillar,size,ship_ob):    # устанавливаем на поле корабль, без обозначения свободных зон
        line = line - 1
        pillar = pillar - 1
        length = abs(size)+1
        if size > 0:
            for i in range(length):
                self.field[line][pillar + i] = ship_ob
        elif size < 0:
            for i in range(length):
                self.field[line + i][pillar] = ship_ob
        elif size == 0:
            self.field[line][pillar] = ship_ob

    def add_ship(self,ship_ob): # добавляет в список корабль в виде объекта
        self.list_ships.append(ship_ob)

    def clear_list_ship(self):      # метод очищает список кораблей
        self.list_ships=[]

    def clear_aroud_ship(self):
        for i in range(height):
            for j in range(width):
                if self.field[i][j] == around_ship:
                    self.field[i][j] = " "

    def num_life(self): # считаем число жизней всех кораблей
        life=0
        for i in range(len(self.list_ships)):
            life = life + self.list_ships[i].life
        return life
    def checks_shot(self,line,pillar,size):     # метод проверяет выстрел. Принимаю аргумент size, прочто потому что фунция выдаёт сразу три числа
        x,y = line,pillar
        line =line-1                                # и возвращает данные, а также меняет состояние поля меняет
        pillar =pillar-1
        size = 0
        if isinstance(self.field[line][pillar],Ships):   # если в данной ячейке объект корабль
            self.field[line][pillar].life -= 1      # то мы минусуем у корабля одну жизнь, как у обекта
            if self.field[line][pillar].life > 0:      # затем проверяем, есть ли жизни ещё
                shot = wounded          # если есть, то возращаем знак ранения по указанным кординатам в виде точки, т.е. size = 0
            else:
                x = self.field[line][pillar].line
                y = self.field[line][pillar].pillar
                size = self.field[line][pillar].size
                shot = killed    #если жизней больше нет, то возвращаем "убит" с координатами корабля и его длинной
            self.field[line][pillar] = wounded      # после получения всех данных от объекта, мы удаляем его из этой ячейки, пометкой ранен
        elif self.field[line][pillar] == miss:  # если мы находим ячейку в которую уже промахивались ничего не меняем, но результат об этом сообщаем в виде W
            shot = "W"
        elif self.field[line][pillar] == cell:  # если пустая, то помечаем промах
            self.field[line][pillar] = miss
            shot = miss
        elif self.field[line][pillar] == around_ship:   # если рядом с бодбитым кораблём, помечаем промахом и сообщаем об этом R
            if self.name == "компьютер":        # помечаем для игрока на поле компьютера
                self.field[line][pillar] = miss     # пометка нужна что бы пользователь видел свои ошибки.
            shot = "R"        # сообщать нужно что бы компьютер повторил попытку
        elif (self.field[line][pillar] == killed) or (self.field[line][pillar] == wounded):
            shot = "K"
        return x,y,size,shot

    def InputShipsComp(self):  # функция расстановки кораблей в рандоме
        attempt = 0     # счётчик количества попыток, расставить корабли
        num_ship = 0
        while (num_ship<NumShip(ship_kol)) and (attempt<1000):  # будем делать попытки пока компьютер не расставит все свои корабли, но не более 1000 раз
            num_ship = 0  # Счётчик всего установленных кораблей. По итогу должен ровняться общему количеству кораблей
            self.clearfield()   # очищаем поле перед новой попыткой
            self.clear_list_ship() # ощищаем список кораблей перед новой попыткой
            for i in range(len(ship_kol),0,-1):
                if ship_kol[i-1] > 0:
                    j = 1   # счтчик установленных кораблей
                    n = 200     # количество попыток, установить корабль
                    while (j<=ship_kol[i-1]) and (n>0):
                        x,y,k = RandomCoordinates(i-1)
                        if self.place_check(x, y, k) == True:
                            ship_object = Ships(x, y, k)
                            self.placement_ship(x, y, k,ship_object)
                            self.add_ship(ship_object)
                            j=j+1
                            num_ship=num_ship+1
                        else:
                            n=n-1
            attempt +=1
        return attempt



class Ships:  # класс корабли
    def __init__(self, line, pillar, size): # конструктор
        self.size = size  # размер корабля или количество палуб
        self.line = line # номер линии с которой начинается корабль, принимает значение "цифра"
        self.pillar = pillar  # номер столбца, с которого начинается корабль, принимает значение "цифра"
        self.life = abs(size)+1 # Количество жизней, будет менять при попадании.
        self.name = ship




# функции для работы
def ShowGame():  # функция вывода игровых полей на экран во время игры
    os.system("cls")
    print("        ПОЛЕ ИГРРОКА ")
    print("       тут ваши корабли и")
    print("    отмечена стрельба по вам ")
    print("")
    player.fieldshow(True)
    print("")
    print("      ПОЛЕ КОМПЬЮТЕРА")
    print("     тут корабли компьютера")
    print("  в это поле стреляете вы")
    print("")
    computer.fieldshow(True)
def Regulations(): # фукция вывода на экран правил и примера заполнения поля
    os.system("cls")
    print(" Пример заполненого поля" )
    print("")
    example.fieldshow(True)
    print(""" Что бы расставить корабли на игровом поле, Вам """)
    print(""" необходимо указать координаты кораблей, поочерёдно """)
    print(""" начиная с больших кораблей. Для понимания, Вам представлен """)
    print(""" пример, на котором координаты трёхпалубного "3A-C" столбики A-C, """)
    print(""" линия 3 . Двухпалубный "5B-6", однапалубный "1B", "d1"  """)
    print(""" Обратите внимание, что сначала цифра или буква, без разницы. Буквы""")
    print(""" латинского алфавита, без пробелов и каких либо символов. Использование  """)
    print(""" симовла " - " обязательно, для расстановки больших кораблей. Корабли  """)
    print(""" не должны косаться друг друга ни бортами, ни углами. Свободная""")
    print(""" зона будет обозначена символом " ~ ". Соответсвенно если во время """)
    print(""" игры Вы увидите такой символ на поле, то стрелять по этим координатам, """)
    print(""" не обязательно, хоть и не запрещено, это такая Вам подсказка.""")
    print(""" Когда будете стрелять по полю противника, Вам также необходимо """)
    print(""" указывать координаты ячейки в которую Вы целитесь, в формате цифра """)
    print(""" и буква (4D, f2 и т.д.). По правилам, при попадании, Вы стреляете""")
    print(""" ещё, пока не промахнётесь. Право первого хода, определяется случайным """)
    print(""" образом. Побеждает тот, кто первый уничтожит корабли противника. """)
    print("")
    input(" Надеюсь правила Вам понятны, тогда нажмите Enter")
    print("")
def Calculation(ships): # Высчитываем общий объём занимаемый кораблями
    q=0
    for i in range(len(ships)):
        q=q+ships[i]*((i+1)*2+3)
    return q
def ShowShips_Kol(): # Вывод списка и количества кораблей
    print(""" Корабли участвующие в игре""")
    for i in range(len(ship_kol),0,-1):
        print(" ",end="")
        for k in range(i):
            print(ship,end="")
        print(" (",i,") - ",ship_kol[i-1]," штук")
def InputSetting(): # функция установки настроек игры
    print(""" Вы находитесь в настройка игры "МОРСКОЙ БОЙ" """)
    global width, height, level, ship_kol # объявляем переменные глобальными
    print("""  """)
    print(""" От размера поля зависит количество и размеры кораблей, которые """)
    print(""" вы сможете расположить на игровом поле. При размерах 8 ячеек и """)
    print(""" более (и в ширину и в высоту), появляется возможность установки """)
    print(""" четырёхпалубного корабля. При размерах 10 и более появиться пяти- """)
    print(""" палубный. При 12, появиться 6-ти палубный. При 14 появиться 7-ми """)
    print(""" палубный. И при 16-ти, появиться 8-ми палубный корабль. """)
    while True: # в этом цикле вводим и проверяем на правильность ширину поля
        try:
            print(""" """)
            ot = int(input(" Введите число столбцов от 6 до 20: "))
        except ValueError:
            print(""" Указать нужно только цифру""")
        else:
            if (type(ot) == int) and (ot >= 6) and (ot <= 20):
                width=ot
                print(""" Ширина игрового поля установлена и равна """,ot)
                break
            print(""" Ввели некоректное значение. Попробуйте ещё раз.""")
            print(""" """)
    while True: # в этом цикле вводим и проверяем на правильность высоту поля
        try:
            print(""" """)
            ot = int(input(" Введите число линий от 6 до 20: "))
        except ValueError:
            print(""" Указать нужно только цифру""")
        else:
            if (type(ot) == int) and (ot >= 6) and (ot <= 20):
                height=ot
                print(""" Высота игрового поля установлена и равна """,ot)
                break
            print(""" Ввели некоректное значение. Попробуйте ещё раз.""")
            print(""" """)

    print(""" """)
    print(""" Теперь необходимо установить сложность игры.""")
    print(""" сложность игры зависит от количества кораблей расположенных на""")
    print(""" игровом поле. Соответственно, чем больше кораблей, тем плотнее """)
    print(""" они расположены на поле, тем легче в них попадать.  """)
    print(""" Уровней сложности всего четыре. Лёгкий от 70% до 90% игрового """)
    print(""" поля заполнены кораблями. Средний = 50-70% заполнения. Сложный  """)
    print(""" = 30-50%. И Трудный = 10-30%. """)
    print(""" Вам нужно указать число от 1 до 4, где 1 - Лёгкий, 4 - Трудный. """)

    while True: # в этом цикле вводим и проверяем на правильность уровень сложности
        try:
            print(""" """)
            ot = int(input(" Введите уровень сложности от 1 до 4: "))
        except ValueError:
            print(""" Указать нужно только цифру""")
        else:
            if (type(ot) == int) and (ot >= 1) and (ot <= 4):
                level=ot
                print(""" Уровень сложности игры установлен и равен """,ot)
                break
            print(""" Ввели некоректное значение. Попробуйте ещё раз.""")
            print(""" """)
    size_field = (width+1)*(height+1) # высчитываем размер поля, что бы понять сколько кораблей можно вместить
                    # плюс один, увеличиваем запас поля, т.е. корабли могут располагаться по краю поля
    if level == 1:
        min_size_field = round(size_field * 0.7)    # Вычисляем допустимые значения заполнения поля
        max_size_field = round(size_field * 0.9)   # в зависимости от сложности игры
    elif level == 2:
        min_size_field = round(size_field * 0.5)
        max_size_field = round(size_field * 0.7)
    elif level == 3:
        min_size_field = round(size_field * 0.3)
        max_size_field = round(size_field * 0.5)
    else:
        min_size_field = round(size_field * 0.1)
        max_size_field = round(size_field * 0.3)
    ship_kol = [0,0,0,0,0,0,0,0] # Обнуляем количество кораблей перед установкой
    a = min(width,height)//2 # высчитывем размер самого большого корабля в зависимости от размера поля
    if a>8: a=8 # ограничиваем размер до 8
    if a < 5: s="х" # хвостики к цифрам
    else: s="и"
    print(""" Теперь устанавливаем количество кораблей.""")
    print(" Вы ввели размер поля %d на %d, соответственно "%(width,height))
    print(" Вам доступен %d-%s палубный корабль и меньше"%(a,s))
    print(""" но не забывайте что количество кораблей ограниченно """)
    print(""" вместимостью морского поля и установленной сложностью""")
    print(""" игры, поэтому програма будет показывать рамки ограничений """)
    print(""" количества кораблей.""")
    t,n,w = 0,2,1 # просто счётчик для расчётов кол-ва кораблей
    for i in range(a,0,-1):  # цикл ввода количества кораблей
        p=round((max_size_field-Calculation(ship_kol))/max_size_field*100)
        n = math.trunc( (1/(i-1+1/i))*(max_size_field-Calculation(ship_kol))/(i*2+3) )
        t = math.trunc((1/(i-1+1/i))*(min_size_field-Calculation(ship_kol))/(i*2+3))-w # -W это возможность не ставить самый большой корабль
        if t<0 : t = 0
        if n<0 : n = 0
        print(""" Для кораблей доступно %d процентов игрового поля"""%p)
        if i > 4: s = "и"
        elif (i<=4) and(i>1): s="x"
        else: s = "а"
        while True:
            print(" %d-%s палубных кораблей можно поставить от %d до %d штук""" %(i,s,t,n))
            try:
                k = int(input(" Введите число кораблей : "))
            except ValueError:
                print(""" Указать нужно только цифру""")
            else:
                if (type(ot) == int) and (k >= t) and (k <= n):
                    print(" %d-%s палубных кораблей %d штук""" % (i, s, k))
                    break
                print(""" Ввели некоректное значение. Попробуйте ещё раз.""")
        print(""" """)
        ship_kol[i-1] = k
        w=0 # обнуляем возможность, т.е. она даётся только для самого большого корабля на текущем поле
    ShowShips_Kol()  # выводим список и количество кораблей
    player.clearfield()  # после изменения настроек, очищае поле, те самым создаём новое с другими размерами
    computer.clearfield()

def InputCoordinates(): # в данной фунции, игрок вводи координаты, которые проверяются на корректность и
    while True:                     # переводятся в число - число. Эта функция подходит для расстановки кораблей
        s=input(" Введите координаты :").upper()            # и для стрельбы
        l=len(s)
        s1,s2="",""
        x1,x2,y1,y2 = 0,0,0,0
        ch = True
        for i in range(l):
            if ord(s[i]) not in valid_characters: ch = False
        if (l<2) or (l>6): # Проверяем длину строки, сразу на корректность ввода
            print(""" Введено не корректное количество символов.""")
        elif s.find(" ") != -1: # Проверяем на пробелы, игрок может его не видеть
            print(""" Пробелов не может быть в координатах""")
        elif (l >= 4) and (l <= 6) and (s.find("-") == -1):  # проверяем наличие "-", в длиных координатах должен быть
            print(""" Ваши координаты не понятны компьютеру. Не вижу разделитель "-" . """)
        elif (l >= 4) and (l <= 6) and (s.count("-") > 1):  # проверяем что бы "-" был только один, мало ли
            print(""" Ваши координаты не понятны компьютеру. Символ "-" должен быть один. """)
        elif (l >= 3) and (l <= 6) and (s[0] == "-") or (s[l-1] == "-"):  # проверяем что бы "-" не был первым или последним
            print(""" Ваши координаты не понятны компьютеру. Символ "-" не может быть первым или последним. """)
        elif ch == False:
            print(""" В координатах присутсвует непонятный компьютеру символ.""")
        else:
            for i in range(l):
                if (ord(s[i])>=48) and (ord(s[i])<=57):
                    s1 = s1+s[i]
                elif (ord(s[i])>=65) and (ord(s[i])<=65+width):
                    s2 = s2+s[i]
                elif (s[i] == "-"):
                    try:
                        x1 = int(s1)
                    except ValueError:
                        x1=0
                    try:
                        y1 = ord(s2)-64
                    except TypeError:
                        y1=0
                    s1,s2 = "",""
            try:
                x2 = int(s1)
            except ValueError:
                x2 = 0
            try:
                y2 = ord(s2)-64
            except TypeError:
                y2 = 0
            if (x1>height) or (x2>height) or (y1>width) or (y2>width):
                print(""" Координаты выходят за границы поля""")
            elif (x1 == 0) and (x2 > 0) and (y1==0) and (y2>0):
                x = x2
                y = y2
                k = 0    # в данном случае указано что одна точка координат
                print(""" Координаты приняты.""")
                break
            elif (x1 == 0) and (x2 > 0) and (y1 > 0) and (y2 > 0):
                x = x2
                y = min(y1,y2)  # берём минимальные, т.е. ищем нос корабля
                k = abs(y1-y2)  # количество точек, длинна корабля. + расположен горизонтально, - вертикально
                print(""" Координаты приняты.""")
                break
            elif (x1 > 0) and (x2 == 0) and (y1 > 0) and (y2 > 0):
                x = x1
                y = min(y1,y2)  # берём минимальные, т.е. ищем нос корабля
                k = abs(y1-y2)  # количество точек, длинна корабля. + расположен горизонтально, - вертикально
                print(""" Координаты приняты.""")
                break
            elif (x1 > 0) and (x2 > 0) and (y1 == 0) and (y2 > 0):
                x = min(x1,x2)
                y = y2
                k = abs(x1-x2)*-1
                print(""" Координаты приняты.""")
                break
            elif (x1 > 0) and (x2 > 0) and (y1 > 0) and (y2 == 0):
                x = min(x1,x2)
                y = y1
                k = abs(x1-x2)*-1
                print(""" Координаты приняты.""")
                break
        print(""" Попробуйте ещё раз внимательнее.""")
    return x,y,k
def InputShips():  # функция расстановки кораблей игроком
    by_new = True
    while by_new == True:
        for i in range(len(ship_kol),0,-1):
            if ship_kol[i-1] > 0:
                j=1
                while j<=ship_kol[i-1]:
                    os.system("cls")
                    print("    Перед Вами ваше игровое поле ")
                    print(" тут надо разместить ваши корабли ")
                    print(" что бы они не касались друг друга")
                    print("")
                    player.fieldshow(True)
                    print("")
                    print(" Раставить нужно: ")
                    ShowShips_Kol()
                    print("")
                    print(" Вам необходимо расставить %d - палубный корабль в количестве %d шт."%(i,ship_kol[i-1]))
                    print(" Укажите координаты корабля №%d"%(j))
                    print("")
                    x,y,k = InputCoordinates()
                    if i != abs(k)+1:
                        print(""" Координаты не соответсвуют длинне корабля""")
                        print(""" Компьютер может подредактировать координаты,""")
                        print(""" либо вы вводите их по новый.""")
                        w = input(" Ввести по новый (Y), оставить компьютеру (нажите Enter)")
                        if w.upper() == "Y":
                            j=j-1
                        else:
                            k=i-1
                            if player.place_check(x, y, k) == True:     # проверяем, возможно ли размещение
                                ship_object = Ships(x, y, k)            # создаём объект корабль
                                player.installation_ships(x, y, k,ship_object)      # ставим объект на поле
                                player.add_ship(ship_object)                # добавляем корабль в список кораблей
                            else:
                                print(""" По указанным координатам корабль не может быть размещён""")
                                print(""" посмотрите внимательнее и укажите координаты ещё раз.""")
                                input(" Нажмите Enter для продолжения")
                                j = j - 1
                    else:
                        if player.place_check(x,y,k) == True:
                            ship_object = Ships(x, y, k)
                            player.installation_ships(x,y,k,ship_object)
                            player.add_ship(ship_object)
                        else:
                            print(""" По указанным координатам корабль не может быть размещён""")
                            print(""" посмотрите внимательнее и укажите координаты ещё раз.""")
                            input(" Нажмите Enter для продолжения")
                            j=j-1
                    j = j+1
        os.system("cls")
        print("  Перед Вами ваше игровое поле ")
        print(" тут Вы разместили ваши корабли ")
        print("")
        player.fieldshow(True)
        print("")
        print(" Если Вас всё устраивает, Enter, и будем играть")
        if input(" хотите расставить по новый, введите N :").upper() != "N":
            by_new = False
            player.clear_aroud_ship()

        else: player.clearfield()   # очищаем поле игрока, если он решил расставить по новый
def RandomCoordinates(size):  # Рандомные координаты в пределах поля
    if size == 0:   # если размер 0, значит нужны координаты точкив (выстрел) в любом месте поля, либо однопалубного корабля
        x = random.randint(1, height)
        y = random.randint(1, width)
        k = size
    else:       # иначе корабль имеет длинну, соответственно рандомим направление
        if random.random()>0.5:
            x=random.randint(1,height-size)   # расположение корабля вертикально. Нет смысла получать координаты носа корабля
            y=random.randint(1,width)       # ниже разницы (высота - длинна), всё равно он не влезет
            k=size*-1       # умножаем на -1, тем самым задаём направление (т.е. вертикальность)
        else:
            x=random.randint(1,height)      # корабль горизонтально
            y=random.randint(1,width-size)
            k=size
    return x,y,k

def NumShip(ships):
    num = 0
    for i in range(len(ships)):
        num=num + ships[i]
    return num


def Battle(): # Фунуция в которой расписан алгоритм битвы
    victory = 0     # переменная обозначающая пбеду
    new_coordinates = True
    x1,y1,x2,y2 = 0,0,0,0
    if random.random()>0.5 :
        player_turn = True
        turn = "игок"
    else:
        player_turn = False
        turn = "компьютер"
    os.system("cls")
    print(" Генератор случайных чисел определил: первым ходит %s"%(turn))
    print("")
    print(""" Перед Вами будет расположенно два поля, сверху поле Ваше,""")
    print(""" снизу поле компьютера. Все ходы компьютера, будут отмечены""")
    print(""" на Вашем поле. Все Ваши ходы, на поле компьютера. При попадании""")
    print(""" по кораблю противника, стреляете сново, при промахе ход переходит.""")
    print(""" Будьте внимательны, выстрел в точку по которой Вы стреляли, не """)
    print(""" является ошибкой, и ход переходит компьютеру, даже если по этим """)
    print(""" координатам расположен корабль, в который Вы попали до того.""")
    print(""" Если Вы ранили корабль противника, вы увидете символ %s. Если"""%(wounded))
    print(""" корабль противника убит, то он обозначится символом %s. Промах = %s ."""%(killed,miss))
    print(""" Поле вокруг убитого корабля обозначается символом %s, не тратьте"""%(around_ship))
    print(""" зря ходы, не стреляйте по этим координатам.""")
    print(""" Побеждает тот, кто первым "потопит" все корабли противника""")
    input(" Желаю удачи. Для начала игры нажмите Enter")
    while victory == 0:
        os.system("cls")
        print(""" Ваше поле с Вашими кораблями""")
        print("")
        player.fieldshow(True)
        print("")
        print(""" Поле компьютера с отметками Ваших промахов и попаданий""")
        print("")
        computer.fieldshow(False)
        if player_turn == True:
            print("")
            print(""" Ваш ход. Подумайте и стреляйте""")
            x,y,k = InputCoordinates()
            x,y,k,shot=computer.checks_shot(x,y,k)
            if shot == miss :
                print(""" Вы промахнулись, ход переходит компьютеру""")
                time.sleep(2)
                player_turn = False
            elif shot == wounded:
                print(""" Попадание, ПОЗДРАВЛЯЮ.""")
                time.sleep(2)
            elif shot == killed:
                print(""" ПОЗДРАВЛЯЮ. Вы потопили корабль""")
                computer.installation_ships(x,y,k,killed)
                time.sleep(2)
            elif shot == "W":
                print(" Вы повторно промахнулись по этой точке. Ход переходит")
                time.sleep(2)
                player_turn = False
            elif shot == "R":
                print(" Зона обозначенная %s всегда пуста, но если Вы желаете "%(around_ship))
                print(" туда стрелять, дело Ваше. Ход переходит.")
                time.sleep(2)
                player_turn = False
            elif shot == "K":
                print(" Какой смысл тратить свои ходы на добивание уже подбитых ")
                print(" кораблей. Ход переходит.")
                time.sleep(2)
                player_turn = False
        else:
            print(""" Ход компьютера. """)
            while True:
                if new_coordinates == True:   # если до этого не было попадания, то компьютер
                    x,y,k = RandomCoordinates(0)        # получает новые рамдомные координаты выстрела
                else:
                    x,y,k = computer_thinks(x1,y1,x2,y2)
                    if x == 0:  # усли по каким-то причинам координаты не получены, то берём рандом
                        new_coordinates = True
                        x1, y1, x2, y2 = 0, 0, 0, 0
                        x, y, k = RandomCoordinates(0)  # получает новые рамдомные координаты выстрела
                x, y, k, shot = player.checks_shot(x,y,k)

                if shot == miss:
                    print(""" Компьютер промахнулся, ход переходит к Вам.""")
                    time.sleep(2)
                    player_turn = True
                    break
                elif shot == wounded:
                    print(""" Попадание компьютером по Ваашему кораблю.""")
                    new_coordinates = False
                    if (x1 == 0) and (y1 == 0):     # если равны нулю, значит не запоминал точку в которую ранил корабль
                        x1,y1 = x,y     # запоминает где ранил
                    else:   # иначе помнит координаты ранения
                        x2, y2 = x, y  # тогда запоминаем последний выстрел
                    time.sleep(2)
                    break
                elif shot == killed:
                    print(""" Ваш корабль потоплен. Не сдавайтесь.""")
                    player.installation_ships(x, y, k, killed)
                    new_coordinates = True
                    x1,y1,x2,y2 = 0,0,0,0
                    time.sleep(2)
                    break
        if player.num_life()==0:
            victory = 1
            os.system("cls")
            print(""" Ваше поле с Вашими кораблями""")
            player.fieldshow(True)
            print("")
            print(""" Поле компьютера с отметками Ваших промахов и попаданий""")
            computer.fieldshow(True)
            print("Компьютер Вас победил")
            input("Для продолжения Enter")
            os.system("cls")
            computer.victory +=1
        if computer.num_life()==0:
            victory = 1
            os.system("cls")
            print(""" Ваше поле с Вашими кораблями""")
            player.fieldshow(True)
            print("")
            print(""" Поле компьютера с отметками Ваших промахов и попаданий""")
            computer.fieldshow(True)
            print("Вы победили компьютер")
            input("Для продолжения Enter")
            os.system("cls")
            player.victory +=1
    player.clear_list_ship()
    computer.clear_list_ship()

def computer_thinks(x1,y1,x2,y2):       # функция в которой компьютер принимает решение, куда ему стрельть после ранени противника.
    x,y,k=0,0,0
    if x2 == 0:
        try:
            if (player.field[x1-1][y1+1-1] != miss) and (player.field[x1-1][y1+1-1] != around_ship): # проверяет, не стоит ли отметка промаха или буферной зоны уже подбитого корабля
                x = x1                                                                              # проверять на наличие свободной ячейки или корабля будет не честно по отношению к игроку
                y = y1+1                                                                            # соответственно прогоняет по кругу все ячейки в которые до этого не стрелял
        except IndexError:
            pass
        try:
            if (x == 0) and ((player.field[x1+1-1][y1-1] != miss) and (player.field[x1+1-1][y1-1] != around_ship)):
                x = x1+1
                y = y1
        except IndexError:
            pass
        try:
            if (x == 0) and (y1-1>=0) and ((player.field[x1-1][y1-1-1] != miss) and (player.field[x1-1][y1-1-1] != around_ship)):
                x = x1
                y = y1-1
        except IndexError:
            pass
        try:
            if (x == 0) and ((player.field[x1-1-1][y1-1] != miss) and (player.field[x1-1-1][y1-1] != around_ship)):
                x = x1-1
                y = y1
        except IndexError:
            pass
    else:       # если x2 не равно 0, значит это второе попадание в раненый корабль.
        if x1 == x2:        # если X-сы равны, значит корабль горизонтально
            try:
                if (x == 0) and ((player.field[x2-1][y2-1+1] != miss) and (player.field[x2-1][y2-1+1] != around_ship) and (player.field[x2-1][y2-1+1] != wounded)):
                    x = x2
                    y = y2+1
            except IndexError:
                pass
            try:
                if (x == 0) and (y2-1-1>=0) and ((player.field[x2-1][y2-1-1] != miss) and (player.field[x2-1][y2-1-1] != around_ship) and (player.field[x2-1][y2-1-1] != wounded)):
                    x = x2
                    y = y2-1
            except IndexError:
                pass
            try:
                if (x == 0) and ((player.field[x2-1][y1-1+1] != miss) and (player.field[x2-1][y1-1+1] != around_ship) and (player.field[x2-1][y1-1+1] != wounded)):
                    x = x2
                    y = y1+1
            except IndexError:
                pass
            try:
                if (x == 0) and (y1-1-1>=0) and ((player.field[x2-1][y1-1-1] != miss) and (player.field[x2-1][y1-1-1] != around_ship) and (player.field[x2-1][y1-1-1] != wounded)):
                    x = x2
                    y = y1-1
            except IndexError:
                pass

        elif y1 == y2:      # либо вертикально
            try:
                if (x == 0) and ((player.field[x2 - 1 + 1][y2 - 1 ] != miss) and (player.field[x2 - 1 +1][y2 - 1] != around_ship) and (player.field[x2 - 1+1][y2 - 1] != wounded)):
                    x = x2+1
                    y = y2
            except IndexError:
                pass
            try:
                if (x == 0) and (x2-1-1>=0) and ((player.field[x2-1-1][y2-1] != miss) and (player.field[x2-1-1][y2-1] != around_ship) and (player.field[x2-1-1][y2-1] != wounded)):
                    x = x2-1
                    y = y2
            except IndexError:
                pass
            try:
                if (x == 0) and ((player.field[x1 - 1 + 1][y2 - 1 ] != miss) and (player.field[x1 - 1 +1][y2 - 1] != around_ship) and (player.field[x1 - 1+1][y2 - 1] != wounded)):
                    x = x1+1
                    y = y2
            except IndexError:
                pass
            try:
                if (x == 0) and (x1-1-1>=0) and ((player.field[x1-1-1][y2-1] != miss) and (player.field[x1-1-1][y2-1] != around_ship) and (player.field[x1-1-1][y2-1] != wounded)):
                    x = x1-1
                    y = y2
            except IndexError:
                pass
    return x,y,k







# Тело основной программы
player = SeaField("игрок",[[cell for m in range(width)] for n in range(height)]) # Создаём объект игрового поля игрока для наглядного вида
computer = SeaField("компьютер",[[cell for m in range(width)] for n in range(height)]) # Создаём объект грового поля компьютера для наглядного вида
example = SeaField("пример",[[around_ship for m in range(20)] for n in range(20)]) # Создаём объект грового поля для примера максимального размера, что бы небыло ошибок Индекса
for i in range(3):  # заполняем пример
    example.field[2][i]=ship
for i in range(2):
    example.field[3][i+4]=ship
    example.field[i+4][1] = ship
example.field[0][3]=ship
example.field[1][5]=ship
example.field[5][4]=ship
example.field[0][1] = ship

os.system("cls")
print(""" Приветствую Вас, на игре "МОРСКОЙ БОЙ". """)
print(""" """)
print(""" Ваш противник искуственный интелект, т.е. компьютер.""")
print(""" По умолчанию настройки выставленны так, что игра будет""")
print(""" проходить на поле размером 6 х 6, с семью кораблями у   """)
print(""" каждого игрока. А именно один трёхпалубный, два двухпалубных""")
print(""" и четыре однопалубных корабля. Сложность игры оцениваю как """)
print(""" "лёгкая" так как корабли расположенны на поле плотно и попасть""")
print(""" в них будет не сложно. Но у Вас есть возможность изменить """)
print(""" настройки. Вы сможете увелить размер поля до 20 х 20, изменить """)
print(""" количество кораблей и изменить сложность игры. Размер игрового  """)
print(""" поля, не обязательно должен быть квадратным, можно и прямоугольным.""")
print("""  """)
print(""" ЖЕЛАЮ ВАМ УДАЧИ""")
print("""  """)

t=False
while t == False:
    print(""" На данный момент побед игрока = %d, и побед компьютера = %d."""% (player.victory,computer.victory))
    print(""" Желаете играть на поле %d х %d, введите "G" или "Game" """%(width,height))
    print(""" Желаете настроить по своему желанию, введите "S" или "Settings"  """)
    print(""" Если Вы передумали играть, для выхода введите "E" или "Exit"  """)
    print("")
    try:
        ot = input(" Что же Вы решили: ")[0].upper()  # Вылавливаем ошибку, когда пользователь нажал Enter без бекв
    except IndexError:
        ot = "y" # При возникновении ошибки, присваиваем любую букву, которая не обрабатывается
    if ot == "G":
        if (player.victory == 0) and (computer.victory == 0):   # Если счёт ноль-ноль, значит игрок играет впервые, то
            Regulations() # Выводит правила игры
        print(""" Можно расставить корабли автоматически, для этого введите A или "Auto" """)
        try:
            ot1 = input(" Если хотите вручную, жмите Enter: ")[0].upper()  # Вылавливаем ошибку, когда пользователь нажал Enter без букв
        except IndexError:
            ot1 = "y"  # При возникновении ошибки, присваиваем любую букву, которая не обрабатывается
        if ot1 == "A":
            k = player.InputShipsComp()
            if k < 1000:
                print(" Компьютер расставил Ваши корабли за %d попыток" % (k))
                player.fieldshow(True)
                time.sleep(2)
            else:
                print(" Компьютер проделал 1000 попыток расставить Ваши корабли, ")
                print(" но у него так и не получилось корректно их выставить. ")
                print(" Попробуйте сделать это самостоятельно. ")
                InputShips() # Игрок расставляет корабли
        else:
            InputShips()    # Игрок расставляет корабли
        print(""" Компьютер расставляет свои корабли. Подождите пожалуйста""")
        k = computer.InputShipsComp()    # схраняем результат работы функции что бы не вызывать её повторно
        if k<1000 :
            print(" Компьютер расставил свои корабли за %d попыток"%(k))
            time.sleep(2)
            Battle()
        else:
            print(" Компьютер проделал 1000 попыток расставить свои корабли, ")
            print(" но у него так и не получилось корректно их выставить. ")
            print(" Возможно плотность кораблей на поле слишком велика, измените ")
            print(" настройки игры, и заходите играть. ")
    elif ot == "S":
        InputSetting()
    elif ot == "E":
        print(""" Всего Вам доброго. Возвращайтесь, поиграем. """)
        time.sleep(2)
        raise SystemExit
    else: print(""" Простите, но Ваше решение не понятно. Попробуйте ещё раз."""), print("")



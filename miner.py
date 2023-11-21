import random


class GamePole:
    __instance = None  # создание единственного игрового поля

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __del__(self):
        GamePole.__instance = None

    def __init__(self, *args):  # (self, N, M, total_mines):
        N = int(args[0][0])
        M = int(args[0][1])
        total_mines = int(args[0][2])
        if total_mines <= M * N:
            self._total_mines = total_mines
            self._pole_cells = tuple(tuple(Cell() for _ in range(M)) for i in range(N))
            self.N = N
            self.M = M
            self._is_win = False
            self._is_loose = False
            self._count_cells = M * N  # общее количество ячеек
            self._open_cells = 0 #число открытых ячеек
        else:
            print('Вы указали слишком большое количество мин. Попробуйте еще раз.')
            start_game()

    def init_pole(self):  # заполнение поля
        for n in self.pole:
            for m in n:
                m._is_open = False
        count_mines = 0
        while count_mines != self._total_mines:  # расстановка мин
            a = random.randint(0, self.N - 1)
            b = random.randint(0, self.M - 1)
            if self.pole[a][b].is_mine == False:
                self.pole[a][b].__dict__['_is_mine'] = True
                count_mines += 1

        for i in range(self.N):  # подсчет количества мин вокруг для каждой пустой ячейки
            for j in range(self.M):
                self.pole[i][j].__dict__['_number'] = self.count_mines(i + 1, j + 1)

    def open_cell(self, i, j):  # раскрытие ячейки
        if i < 0 or j < 0 or i > self.N - 1 or j > self.M - 1:
            raise IndexError('некорректные индексы i, j клетки игрового поля')
        else:
            self.pole[i][j].__dict__['_is_open'] = True

    def count_mines(self, i, j):  # функция подсчета количества мин вокруг ячейки
        count = 0
        first_row = [Cell() for i in range(self.M + 2)]
        new_mat = []
        new_mat.append(first_row)
        for row in self.pole:
            s = [Cell()] + [a for a in row] + [Cell()]
            new_mat.append(s)
        last_row = [Cell() for i in range(self.M + 2)]
        new_mat.append(last_row)
        circle = [new_mat[i - 1][j - 1].is_mine, new_mat[i - 1][j].is_mine,
                  new_mat[i - 1][j + 1].is_mine, new_mat[i][j - 1].is_mine,
                  new_mat[i][j + 1].is_mine, new_mat[i + 1][j - 1].is_mine,
                  new_mat[i + 1][j].is_mine, new_mat[i + 1][j + 1].is_mine]

        count = circle.count(True)
        return count

    def show_pole(self):  # вывод поля в консоль
        show = []
        for row in self.pole:
            new_row = []
            i = self.pole.index(row)
            for item in row:
                j = row.index(item)
                if item.is_open == False:  # нужно дописать фолс
                    new_row.append('#')
                else:
                    if item.is_mine:
                        new_row.append('*')
                    else:
                        count = self.count_mines((i + 1), (j + 1))
                        new_row.append(count)
            show.append(new_row)
        for row in show:
            print(*row)

    @property
    def pole(self):
        return self._pole_cells

    @pole.setter
    def pole(self, value):
        self._pole_cells = value

    def open_empty(self, x, y):
        x1, x2 = (x - 1, x + 2) if x != 0 else (x, x + 2)
        for a in self.pole[x1: x2]:
            y1, y2 = (y - 1, y + 2) if y != 0 else (y, y + 2)
            for i in a[y1:y2]:
                if i.number == 0 and i.is_open == False:
                    i.is_open = True
                    self._open_cells += 1

                    o = a.index(i)
                    k = self.pole.index(a)
                    self.open_empty(k, o)

    def step(self):
        try:
            s = input('Введите координаты ячейки, которую вы хотите открыть через пробел:').split()
            x = int(s[0])
            y = int(s[1])
            if x <= self.N and y <= self.M:
                if self.pole[x][y]._is_open == False:
                    self.pole[x][y]._is_open = True
                    if self.pole[x][y]._is_mine:
                        print('Вы наткнулись на мину и проиграли...')
                        self._is_loose = True
                        answer_new_game()

                    elif self.pole[x][y].number == 0:
                        self.open_empty(x, y)
                        self._open_cells += 1
                    else:
                        self._open_cells += 1

                else:
                    print('Ячейка уже открыта')
            else:
                print('Неверные координаты')
        except:
            print('Пожалуйста, вводите корректные координаты')


class Cell:
    def __init__(self):
        self._is_mine = False
        self._number = 0
        self._is_open = False

    @property
    def is_mine(self):
        return self._is_mine

    @is_mine.setter
    def is_mine(self, val):
        if type(val) != bool:
            raise ValueError("недопустимое значение атрибута")
        else:
            self._is_mine = val

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        if type(value) != int or 0 > value or value > 8:
            raise ValueError("недопустимое значение атрибута")
        else:
            self._number = value

    @property
    def is_open(self):
        return self._is_open

    @is_open.setter
    def is_open(self, value):
        self.__dict__['_is_open'] = value

    def __bool__(self):  # это непонятно зачем, нужно было по заданию
        return self._is_open == False

def answer_new_game():
    s = input('Хотите сыграть еще? д/н?')
    if s in ("д", "н"):
        if s == "д":
            start_game()
    else:
        print('Пожалуйста, ответьте корректно: д/н?')
        answer_new_game()

def new_game():
    game = GamePole(input("Введите желаемые размеры поля и количество мин через пробел:").split())
    game.init_pole()
    while game._is_win == False and game._is_loose == False:
        if game._open_cells == game._count_cells - game._total_mines:
            print('Поздравляю! Вы выйграли!')
            game._is_win = True
            answer_new_game()


        game.show_pole()
        game.step()

    game.show_pole()

def start_game():
    try:
        new_game()
    except:
        print('Пожалуйста, вводите корректные значения')
        new_game()

start_game()
from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Dot{self.x, self.y}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, l, direction, head):
        self.l = l
        self.health = l
        self.head = head
        self.direction = direction

    @property
    def ship_dots(self):
        list_ship_dot = []
        for d in range(self.l):
            d_x = self.head.x
            d_y = self.head.y

            if self.direction == 0:
                d_y += d
            elif self.direction == 1:
                d_x += d

            list_ship_dot.append(Dot(d_x, d_y))
        return list_ship_dot

    def ship_shooten(self, shot):
        return shot in self.ship_dots


class Board:
    def __init__(self, size=6, hide=False):
        self.size = size
        self.hide = hide
        self.field = [["0"] * self.size for _ in range(self.size)]
        self.busy = []
        self.ships = []
        self.count = 0

    def __str__(self):
        all_board = "  | 1 | 2 | 3 | 4 | 5 | 6 |"

        for x, d in enumerate(self.field):
            all_board += f"\n{x + 1} | " + " | ".join(d) + " |"

        if self.hide:
            all_board = all_board.replace("■", "0")
        return all_board

    def out(self, d):
        return not (0 <= d.x < self.size and 0 <= d.y < self.size)

    def countour(self, ship, verb=False):
        square = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.ship_dots:
            for dx, dy in square:
                cell = Dot(d.x + dx, d.y + dy)
                if not(self.out(cell)) and cell not in self.busy:
                    if verb:
                        self.field[cell.x][cell.y] = "*"
                    self.busy.append(cell)

    def add_ship(self, ship):
        for d in ship.ship_dots:
            if d in self.busy or self.out(d):
                raise Exception
        for d in ship.ship_dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.countour(ship)

    def shot(self, dot):
        if self.out(dot):
            raise Exception
        if dot in self.busy:
            raise Exception
        self.busy.append(dot)
        for ship in self.ships:
            if ship.ship_shooten(dot):
                ship.health -= 1
                self.field[dot.x][dot.y] = "X"
                if ship.health == 0:
                    self.countour(ship, verb=True)
                    print("Ship is destroyed")
                    self.count += 1
                    return True
                else:
                    print("Ship is injured")
                    return True
        self.field[dot.x][dot.y] = "*"
        print('missed')
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except Exception as e:
                print(e)


class Computer(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Computer turn{d.x + 1, d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cell = input("Your Turn:").split()

            if len(cell) != 2:
                print("PRINT TWO NUMBERS")
                continue

            x, y = cell

            if not(x.isdigit()) or not(y.isdigit()):
                print("PRINT NUMBERS")
                continue

            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hide = False

        self.ai = Computer(co, pl)
        self.us = User(pl, co)

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(l, randint(0, 1), Dot(randint(0, self.size), randint(0, self.size)))
                try:
                    board.add_ship(ship)
                    break
                except Exception:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def loop(self):
        num = 0
        while True:
            print("-" * 65)
            print("Computer board:", " " * 20, "User Board:")
            print("-" * 65)
            final_bord = ""
            for ai, us in zip(str(self.ai.board).split("\n"), str(self.us.board).split("\n")):
                final_bord += f"{ai}" + " " * 10 + f"{us}\n"
            print(final_bord)
            print("-" * 65)

            if num % 2 == 0:
                print("User turn")
                repeat = self.us.move()
            else:
                print("Computer turn")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 65)
                print("User WIN")
                break

            if self.us.board.count == 7:
                print("-" * 65)
                print("Computer WIN")
                break

            num += 1

    def start(self):
        self.greet()
        self.loop()



g = Game()
g.start()

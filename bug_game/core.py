from .v2d import Point, Vector

from playsound import playsound
import pyraylib as pr
import soundfile as sf
import sounddevice as sd


class Sound:
    def __init__(self, file):
        self.data, self.fs = sf.read(file, dtype='float32')
        self.playing = False

    def play(self, loop=True):
        if not self.playing:
            sd.play(self.data, self.fs, loop=loop)
            self.playing = True

    def stop(self):
        self.playing = False
        sd.stop()


class Button:
    def __init__(self, pos, text=None, image=None, resize_factor=1):
        self.pos = pos
        self.text = text
        self.image = image
        if self.image is not None:
            self.img = pr.Image.load_image(self.image)
            self.img.resize(self.img.width * resize_factor, self.img.height * resize_factor)

    def show(self):
        if self.image is not None:
            self.img.get_texture().draw(
                (
                    self.pos.x - self.img.width / 2,
                    self.pos.y - self.img.height / 2
                )
            )

        if self.text is not None:
            pr.draw_text(self.text["text"], self.pos.x, self.pos.y, self.text["font"], self.text["color"])

    def click(self, mouse, offset=10):
        return self.pos.dist(mouse) < offset


class Candy:
    def __init__(self, pos: Vector, amount: int):
        self.pos = pos
        self.image = "assets/candy.png"
        self.img = pr.Image.load_image(self.image)
        self.img.resize(self.img.width / 10, self.img.height / 10)
        self.amount = amount

    def show(self):
        self.img.get_texture().draw(
            (
                self.pos.point.x - self.img.width / 2,
                self.pos.point.y - self.img.height / 2
            ),
            scale=self.amount / 100,
        )


class Ant:
    def __init__(self, pos: Vector, kind=1):
        self.pos = pos
        self.kind = kind
        self.image = "assets/ant.png"
        self.img = pr.Image.load_image(self.image)
        self.img.resize(self.img.width / 20, self.img.height / 20)

        self.blood_image = "assets/blood.png"
        self.blood_img = pr.Image.load_image(self.blood_image)
        self.blood_img.resize(self.blood_img.width / 10, self.blood_img.height / 10)
        self.let_see = 30

        self.vel = Vector(Point(0, 0))
        self.acc = Vector(Point())

        self.health = self.kind * 2
        self.ate = 0

        self.s = 0

    def __str__(self):
        return f"Ant @ {self.pos.point}"

    def __repr__(self):
        return self.__str__()

    def show(self):
        if self.s > 0:
            self.s -= 1
        if self.health > 0:
            self.move()
            if self.kind == 1:
                c = (0, 0, 255, 255)
            if self.kind == 2:
                c = (0, 255, 0, 255)
            if self.kind == 3:
                c = (255, 0, 0, 255)

            self.img.get_texture().draw(
                (self.pos.point.x - self.img.width / 2,
                 self.pos.point.y - self.img.height / 2),
                rotation=self.vel.heading() + 90,
                color=c,
            )
        else:
            self.blood_img.get_texture().draw(
                (self.pos.point.x - self.img.width / 2,
                 self.pos.point.y - self.img.height / 2),
                rotation=0,
            )
            self.let_see -= 1

    def move(self):
        self.bound()
        self.ate -= 1
        self.vel = self.vel.add(self.acc)
        if self.vel.mag() > (4 - self.kind) * 4:
            self.vel = Vector(Point().from_polar((4 - self.kind) * 4, self.vel.heading()))
        self.pos = self.pos.add(self.vel)

    def force_it(self, candy, mouse):
        self.acc = Vector(Point())
        direction = (candy.pos - self.pos).heading()
        self.acc += Vector(Point().from_polar(0.05, direction))

        if self.pos.point.dist(mouse.point) < 250:
            dir_mouse = (self.pos - mouse).heading()
            self.acc += Vector(Point().from_polar(0.15, dir_mouse))

    def dead(self):
        return self.health <= 0 and self.let_see < 0

    def eat(self, candy, do_play):
        if self.ate <= 0:
            if self.pos.point.dist(candy.pos.point) < 25:
                if do_play:
                    playsound("assets/crunch.wav", False)
                candy.amount -= 1
                self.health += 1
                self.ate = 60

    def bound(self):
        if self.pos.point.x < -200:
            self.pos.point.x = -200
            self.vel = Vector(Point())

        if self.pos.point.x > 1400:
            self.pos.point.x = 1400
            self.vel = Vector(Point())

        if self.pos.point.y < -200:
            self.pos.point.y = -200
            self.vel = Vector(Point())

        if self.pos.point.y > 950:
            self.pos.point.y = 950
            self.vel = Vector(Point())


class Swatter:
    def __init__(self):
        self.image = "assets/swatter.png"
        self.img = pr.Image.load_image(self.image)
        self.img.resize(self.img.width / 5, self.img.height / 5)
        self.stroke = False

        self.img_hit = pr.Image.load_image(self.image)
        self.img_hit.resize(self.img_hit.width / 7, self.img_hit.height / 7)

    def hit(self, ants):
        self.stroke = True
        for ant in ants:
            p = Vector(Point(pr.get_mouse_x(), pr.get_mouse_y()))
            if p.point.dist(ant.pos.point) < 75:
                ant.health -= 1
                ant.vel /= 2

    def unhit(self):
        self.stroke = False

    def show(self, alpha=255):
        if self.stroke:
            self.img_hit.get_texture().draw(
                (pr.get_mouse_x() - self.img.width / 2, pr.get_mouse_y() - self.img.height / 2),
                color=(255, 255, 255, alpha)
            )
        else:
            self.img.get_texture().draw(
                (pr.get_mouse_x() - self.img.width / 2, pr.get_mouse_y() - self.img.height / 2),
                color=(255, 255, 255, alpha)
            )


class Fart:
    def __init__(self, pos):
        self.pos = pos
        self.image = "assets/spray.png"
        self.img = pr.Image.load_image(self.image)
        self.img.resize(self.img.width / 5, self.img.height / 5)
        self.amount = 128

    def kboom(self, ants):
        for ant in ants:
            p = Vector(Point(pr.get_mouse_x(), pr.get_mouse_y()))
            if p.point.dist(ant.pos.point) < (self.img.width / 2 + self.img.height / 2) / 2:
                ant.health = 0

    def show(self):
        if self.amount > 0:
            self.img.get_texture().draw(
                (
                    self.pos.point.x - self.img.width / 2,
                    self.pos.point.y - self.img.height / 2
                ),
                color=[255, 255, 255, self.amount * 2]
            )
            self.amount -= 1

    def delete(self):
        return self.amount <= 0

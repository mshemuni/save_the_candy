import pyraylib as pr
from playsound import playsound

from bug_game import Candy, Ant, Swatter, Fart, Button, Sound
from bug_game import Point, Vector
import math
from random import randint


def main(number_of_candies=1, ants_angle=15, number_of_farts=2):
    difficulty = 1
    diff_text = {0: "  Easy ", 1: " Normal ", 2: "Hard"}
    SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 750
    window = pr.Window((SCREEN_WIDTH, SCREEN_HEIGHT), 'Save The Candy')
    window.set_fps(60)
    window.hide_cursor()

    farts = []

    s = Swatter()

    candies = []
    ants = []

    fart_cool_down = 0
    fn = 0
    hit = False
    start = False
    sound = True
    music = True

    lower_diff = Button(Point(490, 375),
                        text={
                            "text": "<",
                            "font": 24,
                            "color": pr.BLACK
                        },
                        image=None, resize_factor=1)

    raise_diff = Button(Point(620, 375),
                        text={
                            "text": ">",
                            "font": 24,
                            "color": pr.BLACK
                        },
                        image=None, resize_factor=1)

    start_but = Button(Point(820, 375),
                       text={
                           "text": "START",
                           "font": 24,
                           "color": pr.GO_GREEN
                       },
                       image=None, resize_factor=1)

    go_home = Button(Point(450, 400),
                     text={
                         "text": "Go Home",
                         "font": 24,
                         "color": pr.GO_GREEN
                     },
                     image=None, resize_factor=1)

    stop = Button(Point(1075, 25),
                  image="assets/stop.png", resize_factor=0.05)

    sound_on = Button(Point(1175, 25),
                      text=None,
                      image="assets/sound.png",
                      resize_factor=0.075)

    muisc_on = Button(Point(1125, 25),
                      text=None,
                      image="assets/music.png",
                      resize_factor=0.055)

    sound_off = Button(Point(1175, 25),
                       text=None,
                       image="assets/no_sound.png",
                       resize_factor=0.075)

    muisc_off = Button(Point(1125, 25),
                       text=None,
                       image="assets/no_music.png",
                       resize_factor=0.055)

    main_sound = Sound("assets/weird.wav")
    main_sound.play(loop=True)

    while window.is_open():
        window.begin_drawing()
        window.clear_background(pr.LIGHTGRAY)
        mouse = Point(pr.get_mouse_x(), pr.get_mouse_y())

        if sound:
            sound_on.show()
            if pr.is_mouse_button_released(0):
                if sound_on.click(mouse, 15):
                    sound = False
        else:
            sound_off.show()
            if pr.is_mouse_button_released(0):
                if sound_off.click(mouse, 15):
                    sound = True

        if music:
            muisc_on.show()
            if pr.is_mouse_button_released(0):
                if muisc_on.click(mouse, 15):
                    music = False
                    main_sound.stop()
        else:
            muisc_off.show()
            if pr.is_mouse_button_released(0):
                if muisc_off.click(mouse, 15):
                    music = True
                    main_sound.play(loop=True)

        if start:
            stop.show()
            if pr.is_mouse_button_released(0):
                if stop.click(mouse, 15):
                    start = False

            fart_cool_down = max(0, fart_cool_down - 1)
            amount = 0
            for c in candies:
                amount += c.amount

            if amount <= 0:
                pr.draw_text(f'Loser!', 10, 375, 40, pr.RED)
                go_home.show()
                if pr.is_mouse_button_released(0):
                    if go_home.click(mouse, 100):
                        start = False

            elif len(ants) == 0:
                pr.draw_text(f'Winner! Score={amount}', 10, 375, 40, pr.GO_GREEN)
                go_home.show()
                if pr.is_mouse_button_released(0):
                    if go_home.click(mouse, 100):
                        start = False
            else:
                pr.draw_text(f'Right Click to fart. Left click to kill. SAVE THE CANDY!', 10, 10, 24, pr.BLACK)
                pr.draw_text(f'{amount} Candy, {len(ants)} Ant(s) left.', 10, 50, 18, pr.BLACK)
                pr.draw_text(f'{number_of_farts} Farts left. {fart_cool_down} Cool down', 10, 100, 18, pr.BLACK)

                fn += 1
                for c in candies:
                    c.show()

                if pr.is_mouse_button_down(0):
                    if not hit:
                        hit = True
                        s.hit(ants)
                        window.set_fps(60)

                if pr.is_mouse_button_released(0):
                    hit = False
                    s.unhit()

                if pr.is_mouse_button_released(1):
                    if number_of_farts > 0 and fart_cool_down == 0:
                        if sound:
                            playsound("assets/fart.wav", False)
                        fart_cool_down = 100
                        number_of_farts -= 1
                        farts.append(Fart(Vector(mouse)))
                        farts[-1].kboom(ants)

                for nuke_index in range(len(farts) - 1, -1, -1):
                    farts[nuke_index].show()
                    if farts[nuke_index].delete():
                        del farts[nuke_index]

                for ant_index in range(len(ants) - 1, -1, -1):
                    ants[ant_index].show()
                    for c in candies:
                        ants[ant_index].eat(c, sound)
                        ants[ant_index].force_it(c, Vector(mouse))

                    if ants[ant_index].dead():
                        if sound:
                            playsound("assets/tomato.wav", False)
                        del ants[ant_index]
            s.show(255)
        else:
            pr.draw_text(f'SAVE THE CANDY!', 450, 275, 40, pr.BLACK)
            pr.draw_text(f'Difficulty = ', 350, 375, 24, pr.BLACK)
            lower_diff.show()
            pr.draw_text(diff_text[difficulty], 510, 375, 24, pr.BLACK)
            raise_diff.show()
            start_but.show()

            pr.draw_text(f'Ants: https://bit.ly/3I33Wub',
                         860, 550, 16, pr.BLACK)
            pr.draw_text(f'Camdy: https://bit.ly/3G02irj',
                         860, 570, 16, pr.BLACK)
            pr.draw_text(f'Swapper: https://bit.ly/3IgbSsa',
                         860, 590, 16, pr.BLACK)
            pr.draw_text(f'Fart: https://bit.ly/3FZkMIx',
                         860, 610, 16, pr.BLACK)
            pr.draw_text(f'Sound/Music/Stop Icons: https://bit.ly/3o4eroT',
                         860, 630, 16, pr.BLACK)
            pr.draw_text(f'Paste sound: https://bit.ly/3xFUW9p',
                         860, 650, 16, pr.BLACK)
            pr.draw_text(f'Fart Sound: https://bit.ly/3p735jo',
                         860, 670, 16, pr.BLACK)
            pr.draw_text(f'Crunch Sound: https://bit.ly/32KFJIW',
                         860, 690, 16, pr.BLACK)
            pr.draw_text(f'Music: https://www.beepbox.co',
                         860, 710, 16, pr.BLACK)

            pr.draw_text("How to play:\n"
                         "Don't let ants eat our candy. Left click to kill them\n"
                         "They have stamina. To kill them you might need multiple strokes.\n"
                         "Once they eat they get stronger.\n"
                         "They don't like the swapper. They'll run away from it.\n"
                         "Right click can kill multiple ants.\n"
                         "But you have limited stroke and there will be a cool down.",
                         10, 500, 22, pr.BLACK)

            if pr.is_mouse_button_released(0):

                if lower_diff.click(mouse, 30):
                    difficulty = max(0, difficulty - 1)

                if raise_diff.click(mouse, 30):
                    difficulty = min(2, difficulty + 1)

                if start_but.click(mouse, 120):
                    start = True
                    if difficulty == 2:
                        number_of_candies = 2
                        ants_angle = 5
                        number_of_farts = 3
                    elif difficulty == 1:
                        number_of_candies = 1
                        ants_angle = 10
                        number_of_farts = 4
                    else:
                        number_of_candies = 1
                        ants_angle = 15
                        number_of_farts = 2

                    candies = [
                        Candy(Vector(
                            Point(
                                pr.get_random_value(SCREEN_WIDTH / 4, 3 * SCREEN_WIDTH / 4),
                                pr.get_random_value(SCREEN_HEIGHT / 4, 3 * SCREEN_HEIGHT / 4),
                            )
                        ), 100)
                        for _ in range(number_of_candies)
                    ]
                    ants = [
                        Ant(
                            Vector(
                                Point(
                                    randint(-50, 50) + (SCREEN_WIDTH / 2) * (math.cos(math.radians(ang)) + 1),
                                    randint(-50, 50) + (SCREEN_HEIGHT / 2) * (math.sin(math.radians(ang)) + 1)
                                )
                            ),
                            kind=randint(1, 3)
                        )
                        for ang in range(0, 360, ants_angle)
                    ]

            s.show(150)

        window.end_drawing()

    window.show_cursor()
    window.close()


if __name__ == '__main__':
    main(1, 15, 3)

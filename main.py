import pygame as pg
from pygame.math import Vector2

WSIZE = (720, 480)

screen = pg.display.set_mode(WSIZE)

point_r = 6


def intrpolation_logranje(points, x):
    res = 0
    for i in range(len(points)):
        mul = 1
        for k in range(len(points)):
            if k == i:
                continue
            mul *= (x - points[k].x) / (points[i].x - points[k].x)
        res += points[i].y * mul
    return res


class Spline:
    def __init__(self, points):
        self.points = points

    def draw(self, surface, color="white", colorl="yellow"):
        last_point = None
        for point in self.points:
            pg.draw.circle(surface, color, point, point_r, 2)
            if last_point:
                pg.draw.line(surface, colorl, last_point, point, 2)
                self.draw_lorange(surface, color, last_point, point)
            last_point = point

    def draw_lorange(self, surface, color, last_point, point):
        # logranje intrpoloation
        x1, x2 = min(point.x, last_point.x), max(point.x, last_point.x)
        for x in range(int(x1), int(x2)):
            pos = x, intrpolation_logranje(self.points, x)
            pg.draw.circle(surface, color, pos, 1)




def main():
    spline = Spline([Vector2(10, 10)])
    grabbed_point: Vector2 = None
    running = True
    while running:
        screen.fill("black")
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_MIDDLE:
                    spline.points.append(Vector2(event.pos))
                elif event.button == pg.BUTTON_LEFT and grabbed_point is None:
                    for point in spline.points:
                        if pg.Rect(point.x - point_r, point.y - point_r, point_r * 2, point_r * 2).collidepoint(
                                event.pos):
                            grabbed_point = point
                            break
            elif event.type == pg.MOUSEMOTION:
                if grabbed_point:
                    grabbed_point.xy = event.pos
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == pg.BUTTON_LEFT and grabbed_point:
                    grabbed_point = None

        spline.draw(surface=screen)
        pg.display.flip()


if __name__ == '__main__':
    main()

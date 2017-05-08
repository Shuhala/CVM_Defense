import math


class Helper(object):
    def get_angled_point(angle, longueur, cx, cy):
        x = (math.cos(angle) * longueur) + cx
        y = (math.sin(angle) * longueur) + cy
        return (x, y)

    get_angled_point = staticmethod(get_angled_point)

    def calc_angle(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        angle = (math.atan2(dy, dx))  # % (2*math.pi)) * (180/math.pi)
        return angle

    calc_angle = staticmethod(calc_angle)

    def calc_distance(x1, y1, x2, y2):
        dx = abs(x2 - x1) ** 2
        dy = abs(y2 - y1) ** 2
        distance = math.sqrt(dx + dy)
        return distance

    calc_distance = staticmethod(calc_distance)

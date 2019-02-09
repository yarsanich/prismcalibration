from typing import NamedTuple
from math import sqrt


class Point(NamedTuple):
    x: int  # Ignore PEP8Bear
    y: int

    def __repr__(self):
        return str((self.x, self.y))

    def __str__(self):
        return str((self.x, self.y))


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def normal(self, turn_direction="left"):
        if turn_direction == "left":
            x = - self.y
            y = self.x
        elif turn_direction == "right":
            x = self.y
            y = - self.x
        else:
            return None
        return Vector(x, y)


class Line:
    def __init__(self, normal_vector: Vector=Vector(0, 0), point: Point=Point(0, 0)):
        """Line is saved in form y = k * x + b ."""
        self.normal_vector = normal_vector
        self.point = point

    def parameter_form(self):
        a, b, c = self.parameters()
        return " ".join([str(a) + "x",
                         "+",
                         "(" + str(b) + "y" + ")",
                         "=",
                         str(c)])

    def direction_vector(self):
        return self.normal_vector.normal()

    def parameters(self):
        """Return parameters from parameter form a * x + b * y = c"""
        coeff = (self.normal_vector.x * self.point.x 
                 + self.normal_vector.y * self.point.y)
        return (self.normal_vector.x, self.normal_vector.y, coeff)

    @classmethod
    def from_two_points(cls, point_1, point_2):
        normal_vector = Vector(point_1.y - point_2.y, point_2.x - point_1.x)
        return cls(normal_vector, point_1)


class LineSection(Line):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.point_2 = Point(0, 0)
    
    @classmethod
    def from_two_points(cls, point_1, point_2):
        normal_vector = Vector(point_1.y - point_2.y, point_2.x - point_1.x)
        line_section = cls(normal_vector, point_1)
        line_section.point_2 = point_2
        return line_section


def intersection_of_two_lines(line_1, line_2):
    """
    We have linear system:

    A1 * x + B1 * y = C1
    A2 * x + B2 * y = C2

    let's do it with Cramer's rule, so solution can be found in determinants:

    x = Dx/D
    y = Dy/D

    where D is main determinant of the system:

    A1 B1
    A2 B2

    and Dx and Dy can be found from matricies:

    C1 B1
    C2 B2

    and

    A1 C1
    A2 C2

    """
    a_1, b_1, c_1 = line_1.parameters()
    a_2, b_2, c_2 = line_2.parameters()
    
    d = a_1 * b_2 - b_1 * a_2
    d_x = c_1 * b_2 - b_1 * c_2
    d_y = a_1 * c_2 - c_1 * a_2
    
    if d != 0:
        # intersection point
        x = d_x / d
        y = d_y / d
        return Point(x, y)
    return None


def parallel_two_lines(line_1, line_2):
    normal_vector_1 = line_1.normal_vector
    normal_vector_2 = line_2.normal_vector

    if (normal_vector_1.x / normal_vector_2.x 
        - normal_vector_1.y / normal_vector_2.y) == 0:
        return True
    return False


def distance_between_two_points(point_1: Point, point_2: Point):
    return sqrt((point_2.x - point_1.x) ** 2 + (point_2.y - point_1.y) ** 2)


def distance_between_two_lines(line_1, line_2):
    if not parallel_two_lines(line_1, line_2):
        return 0
    # Define normal vector for normal line between of input lines
    # it is direction vector of first(or second) line
    normal_vector = line_1.direction_vector()
    point = line_1.point
    normal_line = Line(normal_vector, point)
    
    intersection_point_1 = intersection_of_two_lines(line_1, normal_line)
    intersection_point_2 = intersection_of_two_lines(line_2, normal_line)
    return distance_between_two_points(intersection_point_1,
                                       intersection_point_2)


def point_on_line(point: Point, line: Line) -> bool:
    a, b, c = line.parameters()
    if a * point.x + b * point.y == c:
        return True
    return False


def point_on_line_section(point: Point, line_section: LineSection) -> bool:
    if not point_on_line(point, line_section):
        return False
    if abs(line_section.point.x) <= abs(point.x) <= abs(line_section.point_2.x):
        return True
    return False


def line_section_contain_line_section(line_section_1: LineSection,
                                      line_section_2: LineSection) -> bool:
    """Return True if line_section_1 contains line_section_2, else False."""
    if not (parallel_two_lines(line_section_1, line_section_2)
            and distance_between_two_lines(line_section_1, line_section_2)):
        return False
    if (point_on_line_section(line_section_2.point, line_section_1)
        and point_on_line_section(line_section_2.point_2, line_section_1)):
        return True
    return False


def combine_two_line_sections(line_section_1: LineSection,
                              line_section_2: LineSection):
    if distance_between_two_lines(line_section_1, line_section_2) != 0:
        # Line sections aren't on the same line
        print(distance_between_two_lines(line_section_1, line_section_2))
        return None
    # if line_section_contain_line_section(line_section_1, line_section_2):
    #     # line_section_1 contains line_section_2
    #     return line_section_1
    # if line_section_contain_line_section(line_section_2, line_section_1):
    #     # line_section_2 contains line_section_1
    #     return line_section_2
    # four points(ends of line sections)
    points = [line_section_1.point, line_section_1.point_2,
              line_section_2.point, line_section_2.point_2]
    points = sorted(points, key=lambda p: abs(p.x))
    return LineSection.from_two_points(points[0], points[-1])


if __name__ == "__main__":
    point_1, point_2 = Point(4, 1), Point(6, 3)
    # line_1 = Line.from_two_points(point_1, point_2)
    line_section_1 = LineSection.from_two_points(point_1, point_2)
    
    point_3, point_4 = Point(5, 1), Point(7, 3)
    # line_2 = Line.from_two_points(point_3, point_4)
    line_section_2 = LineSection.from_two_points(point_3, point_4)
    
    test_point = Point(5, 2)
    # print(point_on_line_section(test_point, line_section_1))
    # print(point_on_line_section(test_point, line_section_2))
    
    point_5, point_6 = Point(1, 1), Point(5, 5)
    line_section_3 = LineSection.from_two_points(point_5, point_6)
    
    point_7, point_8 = Point(3, 3), Point(6, 6)
    line_section_4 = LineSection.from_two_points(point_7, point_8)
    combined_line_section = combine_two_line_sections(line_section_3,
                                                      line_section_4)
    print(combined_line_section.point, combined_line_section.point_2)

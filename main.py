import pygame
import random
import math
import functools

pygame.init()
screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Convex Hull")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


def find_side(p1, p2, p):
    check = ((p1[0] - p[0]) * (p2[1] - p[1])) - \
        ((p2[0] - p[0]) * (p1[1] - p[1]))

    if check > 0:
        return 1  # Left side
    elif check < 0:
        return -1  # Right side
    else:
        return 0  # Collinear


def solve_convex_hull(a, p1, p2, side, resultPoints):
    index = -1
    maxDistance = 0

    for i in range(len(a)):
        temp = abs(
            ((p2[1] - p1[1]) * a[i][0])
            - ((p2[0] - p1[0]) * a[i][1])
            + (p2[0] * p1[1])
            - (p2[1] * p1[0])
        ) / math.sqrt(pow((p2[1] - p1[1]), 2) + pow((p2[0] - p1[0]), 2))

        if find_side(p1, p2, a[i]) == side and temp > maxDistance:
            index = i
            maxDistance = temp

    if index == -1:
        point1 = (p1[0], p1[1])
        point2 = (p2[0], p2[1])

        if point1 not in resultPoints:
            resultPoints.append(point1)

        if point2 not in resultPoints:
            resultPoints.append(point2)
    else:
        solve_convex_hull(a, p1, a[index], find_side(
            a[index], p1, p2), resultPoints)
        solve_convex_hull(a, p2, a[index], find_side(
            a[index], p2, p1), resultPoints)


def compare_points(point, center_point):
    x, y = point[0] - center_point[0], point[1] - center_point[1]
    angle = math.atan2(y, x)
    return angle

# def cmp_sort(a, b, centerPoint):
#     if a[0] - centerPoint[0] >= 0 and b[0] - centerPoint[0] < 0:
#         return True
#     elif a[0] - centerPoint[0] < 0 and b[0] - centerPoint[0] >= 0:
#         return False

#     if a[0] - centerPoint[0] == 0 and b[0] - centerPoint[0] == 0:
#         if a[1] - centerPoint[1] >= 0 or b[1] - centerPoint[1] >= 0:
#             return a[1] > b[1]
#         return b[1] > a[1]

#     det = (a[0] - centerPoint[0]) * (b[1] - centerPoint[1]) - (b[0] - centerPoint[0]) * (a[1] - centerPoint[1])
#     if det < 0:
#         return True
#     if det > 0:
#         return False

#     d1 = (a[0] - centerPoint[0]) * (a[0] - centerPoint[0]) + (a[1] - centerPoint[1]) * (a[1] - centerPoint[1])
#     d2 = (b[0] - centerPoint[0]) * (b[0] - centerPoint[0]) + (b[1] - centerPoint[1]) * (b[1] - centerPoint[1])

#     return d1 > d2


def draw_lines(resultPoints):
    if len(resultPoints) > 0:
        scaled_points = [(screen_width // 2 + point[0],
                          screen_height // 2 - point[1]) for point in resultPoints]
        scaled_points.append(scaled_points[0])
        for i in range(len(scaled_points) - 1):
            pygame.draw.line(
                screen, BLUE, scaled_points[i], scaled_points[i + 1], 3)


def draw_input_box(user_text):
    font = pygame.font.Font(None, 18)
    input_rect = pygame.Rect(5, 5, 140, 20)
    color = pygame.Color('white')
    pygame.draw.rect(screen, color, input_rect, 2)
    text_surface = font.render(user_text, True, ('white'))
    screen.blit(text_surface, (input_rect.x + 3, input_rect.y + 3))
    input_rect.w = max(100, text_surface.get_width() + 10)


def draw_message(message, type= None):
    font = pygame.font.Font(None, 18)
    text_surface = font.render(message, True, ('red')) if type == 'error' else font.render(message, True, ('black'))
    text_rect = text_surface.get_rect(
        center=(screen_width // 2, screen_height-20))
    background_rect = pygame.Rect(
        text_rect.left - 10,
        text_rect.top - 10,
        text_rect.width + 20,
        text_rect.height + 20
    )
    pygame.draw.rect(screen, (255, 255, 255), background_rect)
    screen.blit(text_surface, text_rect)


def draw_cartesian():
    pygame.draw.line(screen, WHITE, (0, screen_height // 2),
                     (screen_width, screen_height // 2), 3)
    pygame.draw.line(screen, WHITE, (screen_width // 2, 0),
                     (screen_width // 2, screen_height), 3)


def draw_points(vectorPoint):
    for point in vectorPoint:
        scaled_point = (screen_width // 2 +
                        point[0], screen_height // 2 - point[1])
        pygame.draw.circle(screen, RED, scaled_point, 4)


def main():
    vectorPoint = []
    resultPoints = []
    centerPoint = None
    user_text = ''

    running = True
    can_do_hull = False
    draw_error = False
    message = ''
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    numPoints = int(user_text)
                    user_text = ''
                    can_do_hull = True
                    draw_error = False
                else:
                    user_text += event.unicode

        screen.fill(BLACK)
        draw_input_box(user_text)
        draw_cartesian()
        draw_lines(resultPoints)
        draw_points(vectorPoint)
        if (draw_error):
            draw_message(message, 'error')
        pygame.display.flip()
        clock.tick(60)

        if can_do_hull:
            resultPoints = []
            vectorPoint = []
            i = 0
            if numPoints == 1:
                draw_error = True
                message = 'Nao eh possivel criar um casco convexo com apenas 1 ponto'

            elif numPoints == 2:
                draw_error = True
                message = 'Nao eh possivel criar um casco convexo com apenas 2 pontos'
            else:    
                while i < numPoints:
                    found = False
                    while not found:
                        xTemp = random.randint(-250, 250)
                        yTemp = random.randint(-250, 250)
                        tempPoint = (xTemp, yTemp)

                        if tempPoint not in vectorPoint:
                            found = True
                            vectorPoint.append(tempPoint)
                            print(f"Random result = ({xTemp}, {yTemp})")
                            i += 1

                centerPointX = sum(point[0]
                                for point in vectorPoint) // len(vectorPoint)
                centerPointY = sum(point[1]
                                for point in vectorPoint) // len(vectorPoint)
                centerPoint = (centerPointX, centerPointY)
                indexXMin = min(range(numPoints),
                                key=lambda i: vectorPoint[i][0])
                indexXMax = max(range(numPoints),
                                key=lambda i: vectorPoint[i][0])
                solve_convex_hull(
                    vectorPoint, vectorPoint[indexXMin], vectorPoint[indexXMax], 1, resultPoints)
                solve_convex_hull(
                    vectorPoint, vectorPoint[indexXMin], vectorPoint[indexXMax], -1, resultPoints)
                resultPoints.sort(
                    key=lambda point: compare_points(point, centerPoint))
                print("Convex hull result:")
                for point in resultPoints:
                    print(point)
            can_do_hull = False
    pygame.quit()


if __name__ == "__main__":
    main()

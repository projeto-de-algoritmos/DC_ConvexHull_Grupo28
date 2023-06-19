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

vectorPoint = []
resultPoints = []
centerPoint = None
allBaseLines = []


def get_distance(cpt, bl):
    Vy = bl[1][0] - bl[0][0]
    Vx = bl[0][1] - bl[1][1]
    return (Vx * (cpt[0] - bl[0][0]) + Vy * (cpt[1] - bl[0][1]))


def find_most_distant_point_base_line(baseLine, points):
    maxD = 0
    maxPt = []
    newPoints = []
    for pt in points:
        d = get_distance(pt, baseLine)
        if d > 0:
            newPoints.append(pt)
        else:
            continue
        if d > maxD:
            maxD = d
            maxPt = pt
    return {'maxPoint': maxPt, 'newPoints': newPoints}


def build_convex_hull(baseLine, points):
    allBaseLines.append(baseLine)
    convexHullBaseLines = []
    t = find_most_distant_point_base_line(baseLine, points)
    if len(t['maxPoint']) > 0:  # if there is still a point "outside" the base line
        convexHullBaseLines.extend(
            build_convex_hull([baseLine[0], t['maxPoint']], t['newPoints'])
        )
        convexHullBaseLines.extend(
            build_convex_hull([t['maxPoint'], baseLine[1]], t['newPoints'])
        )
        return convexHullBaseLines
    else:  # if there is no more point "outside" the base line, the current base line is part of the convex hull
        return [baseLine]


def get_convex_hull(points):
    # find first baseline
    maxX, minX = float('-inf'), float('inf')
    maxPt, minPt = None, None
    for pt in points:
        if pt[0] > maxX or maxX is None:
            maxPt = pt
            maxX = pt[0]
        if pt[0] < minX or minX is None:
            minPt = pt
            minX = pt[0]
    ch = build_convex_hull([minPt, maxPt], points) + \
        build_convex_hull([maxPt, minPt], points)
    return ch


def draw_lines(resultPoints):
    scaled_points = []
    if len(resultPoints) > 2:
        for line in resultPoints:
            scaled_points.append(
                (screen_width // 2 + line[0][0], screen_height // 2 - line[0][1]))
            scaled_points.append(
                (screen_width // 2 + line[1][0], screen_height // 2 - line[1][1]))
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


def draw_message(message, type=None):
    font = pygame.font.Font(None, 18)
    text_surface = font.render(
        message, True, ('red')) if type == 'error' else font.render(message, True, ('black'))
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
    global vectorPoint, resultPoints, centerPoint, allBaseLines
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
                    draw_error = False
                    if not user_text.isdigit():
                        draw_error = True
                        message = 'insira apenas numeros'
                    else:    
                        numPoints = int(user_text)
                        can_do_hull = True
                    user_text = ''
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
            allBaseLines = []
            vectorPoint = []
            i = 0
            if numPoints <= 0:
                draw_error = True
                message = 'Insira numeros superiores a 2'
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
                resultPoints = get_convex_hull(vectorPoint)
                print("Convex hull result:")
                for point in resultPoints:
                    print(point)
            can_do_hull = False
    pygame.quit()


if __name__ == "__main__":
    main()

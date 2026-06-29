import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wrestling Visual Sim")

font = pygame.font.SysFont(None, 36)

# wrestlers
p1 = {"x": 200, "y": 200, "score": 0}
p2 = {"x": 600, "y": 200, "score": 0}

clock = pygame.time.Clock()

def attempt_attack(attacker, defender):
    if random.random() > 0.5:
        attacker["score"] += 1

running = True
frame = 0

while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # simulate match every ~60 frames
    if frame % 60 == 0:
        attempt_attack(p1, p2)
        attempt_attack(p2, p1)

    # draw wrestlers
    pygame.draw.circle(screen, (0, 200, 255), (p1["x"], p1["y"]), 30)
    pygame.draw.circle(screen, (255, 100, 100), (p2["x"], p2["y"]), 30)

    # score display
    text = font.render(f"P1: {p1['score']}  P2: {p2['score']}", True, (255,255,255))
    screen.blit(text, (20, 20))

    pygame.display.flip()
    clock.tick(60)
    frame += 1

pygame.quit()
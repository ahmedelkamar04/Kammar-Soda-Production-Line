import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1100, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KAMAR SODA HMI")

NAVY = (8, 27, 47)
ORANGE = (217, 98, 38)
WHITE = (245, 245, 242)
CARD = (255, 255, 255)
TEXT = (15, 23, 42)
GRAY = (110, 120, 130)
GREEN = (20, 170, 80)
RED = (220, 40, 40)
BLUE = (45, 125, 230)

title_font = pygame.font.SysFont("Arial", 40, bold=True)
heading_font = pygame.font.SysFont("Arial", 26, bold=True)
normal_font = pygame.font.SysFont("Arial", 21)
small_font = pygame.font.SysFont("Arial", 17)

running = False
produced = 50
defective = 5
good = produced - defective

current_alarm = "No Active Alarms"
station_index = 0
last_alarm = "No Active Alarms"

stations = [
    "Bottle Blow",
    "Soda Fill",
    "Carbonation",
    "Cap On",
    "Label",
    "QC & Pack"
]

alarms = [
    "Underfilled Bottle",
    "Missing Cap",
    "Missing Label",
    "Low Carbonation",
    "Bottle Jam",
    "Quality Check Failed"
]

start_btn = pygame.Rect(70, 615, 150, 50)
stop_btn = pygame.Rect(245, 615, 150, 50)
reset_btn = pygame.Rect(420, 615, 150, 50)
emergency_btn = pygame.Rect(740, 615, 290, 50)

clock = pygame.time.Clock()
timer = 0


def draw_text(text, font, color, x, y):
    screen.blit(font.render(text, True, color), (x, y))


def draw_card(x, y, w, h, title, value, color):
    pygame.draw.rect(screen, CARD, (x, y, w, h), border_radius=12)
    draw_text(title, small_font, GRAY, x + 18, y + 16)
    draw_text(value, heading_font, color, x + 18, y + 48)


def draw_button(rect, text, color):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    label = heading_font.render(text, True, WHITE)
    screen.blit(label, (
        rect.x + (rect.width - label.get_width()) // 2,
        rect.y + (rect.height - label.get_height()) // 2
    ))


while True:
    dt = clock.tick(60)
    timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if event.type == pygame.MOUSEBUTTONDOWN:
        if start_btn.collidepoint(event.pos):
         running = True
    last_alarm = "No Active Alarms"

    if stop_btn.collidepoint(event.pos):
                running = False

    if reset_btn.collidepoint(event.pos):
                running = False
                produced = 0
                defective = 0
                good = 0
                station_index = 0
                last_alarm = "No Active Alarms"

    if emergency_btn.collidepoint(event.pos):
                running = False
                last_alarm = "Emergency Stop Activated"

    if running and timer > 900:
        timer = 0
        station_index = (station_index + 1) % len(stations)

        if station_index == 0:
            produced += 1

            if random.random() < 0.10:
                defective += 1
                last_alarm = random.choice(alarms)
            else:
                last_alarm = "No Active Alarms"

            good = produced - defective

    efficiency = round((good / produced) * 100, 1) if produced > 0 else 0
    defect_rate = round((defective / produced) * 100, 1) if produced > 0 else 0
    
    screen.fill(WHITE)

    pygame.draw.rect(screen, NAVY, (0, 0, WIDTH, 110))
    pygame.draw.rect(screen, ORANGE, (0, 106, WIDTH, 4))

    draw_text("KAMAR SODA", title_font, WHITE, 45, 25)
    draw_text("Carbonated Soft-Drink Production Line HMI", normal_font, (210, 220, 230), 48, 72)

    status_color = GREEN if running else RED
    status_text = "RUNNING" if running else "STOPPED"
    pygame.draw.circle(screen, status_color, (895, 45), 12)
    draw_text(status_text, heading_font, WHITE, 925, 30)

    draw_card(55, 135, 220, 100, "Produced Bottles", str(produced), BLUE)
    draw_card(305, 135, 220, 100, "Good Bottles", str(good), GREEN)
    draw_card(555, 135, 220, 100, "Defective Bottles", str(defective), RED)
    draw_card(805, 135, 220, 100, "Defect Rate", f"{defect_rate}%", ORANGE)
    draw_card(805, 245, 220, 100, "Efficiency", f"{efficiency}%", ORANGE) 

    pygame.draw.rect(screen, CARD, (55, 260, 450, 110), border_radius=12)
    draw_text("Plant Information", heading_font, TEXT, 75, 278)
    draw_text("Plant: KAMAR SODA", normal_font, TEXT, 75, 315)
    draw_text("Shift: A", normal_font, TEXT, 75, 345)
    draw_text("Operator: Ahmed", normal_font, TEXT, 240, 345)

    pygame.draw.rect(screen, CARD, (540, 260, 485, 110), border_radius=12)
    draw_text("Active Alarms", heading_font, RED, 560, 278)

    alarm_color = GREEN if last_alarm == "No Active Alarms" else RED
    draw_text(last_alarm, normal_font, alarm_color, 560, 325)

    pygame.draw.rect(screen, CARD, (55, 395, 970, 190), border_radius=14)
    draw_text("Production Flow", heading_font, TEXT, 80, 412)
    draw_text(f"Current Station: {stations[station_index]}", normal_font, GRAY, 80, 448)

    start_x = 95
    y = 505

    for i, station in enumerate(stations):
        x = start_x + i * 160

        color = GREEN if i == station_index and running else NAVY
        pygame.draw.circle(screen, color, (x + 62, y - 25), 9)
        pygame.draw.rect(screen, color, (x, y, 125, 50), border_radius=8)

        label = small_font.render(station, True, WHITE)
        screen.blit(label, (x + (125 - label.get_width()) // 2, y + 15))

        if i < len(stations) - 1:
            pygame.draw.line(screen, ORANGE, (x + 125, y + 25), (x + 155, y + 25), 4)
            pygame.draw.polygon(screen, ORANGE, [
                (x + 155, y + 25),
                (x + 145, y + 17),
                (x + 145, y + 33)
            ])

    draw_button(start_btn, "START", GREEN)
    draw_button(stop_btn, "STOP", RED)
    draw_button(reset_btn, "RESET", BLUE)
    draw_button(emergency_btn, "EMERGENCY STOP", ORANGE)

    draw_text(f"Production Rate: {produced * 12} bottles/hr", small_font, GRAY, 70, 680)

    pygame.display.update()
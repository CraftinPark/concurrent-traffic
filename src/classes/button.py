import pygame

class Button:

    def __init__(self, screen: pygame.Surface, color: tuple[int, int, int], hover_color: tuple[int, int, int], start_point: tuple[int, int], dim: tuple[int, int], text: str, on_click=None, cargs=()) -> None:
        self.screen = screen
        self.color = color
        self.hover_color = hover_color
        self.x = start_point[0]
        self.y = start_point[1]
        self.width = dim[0]
        self.height = dim[1]
        self.text = text
        self.on_click = on_click
        self.cargs = cargs

    def is_selected(self) -> bool:
        mouse = pygame.mouse.get_pos()
        return self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height

    def click(self) -> None:
        if self.is_selected() and self.on_click:
            self.on_click(*self.cargs)

    def draw(self) -> None:
        pygame.draw.rect(self.screen, self.hover_color if self.is_selected() else self.color, [self.x , self.y, self.width, self.height])
        if self.text != '':
            font = pygame.font.SysFont('corbel', 30)
            text = font.render(self.text, 1, (255, 255, 255))
            self.screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
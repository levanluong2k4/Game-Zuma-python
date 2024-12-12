import math
from game.Params import *
from game.ui import BONUS_IMAGES
import game.images


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, pos_in_path, path):
        pygame.sprite.Sprite.__init__(self)

        self.color = color

        self.path = path
        self.pos_in_path = pos_in_path

        self.image = pygame.Surface(BALL_SIZE)
        self.pos = self.path.positions[self.pos_in_path]
        self.rect = self.image.get_rect(center=(round(self.pos.x),
                                                round(self.pos.y)))

        self.can_move = True
        self.bonus = None

    def set_bonus(self, bonus):
        self.bonus = bonus

    def set_position(self, pos_in_path):
        self.pos_in_path = pos_in_path
        self.pos = self.path.positions[self.pos_in_path]
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def update(self):
        if self.can_move:
            self.move(1)

    def move(self, steps):
        # pos_in_path = pos_in_path + steps
    # (Cập nhật vị trí hiện tại trong chuỗi đường đi)
        self.pos_in_path += steps
        
        # If pos_in_path >= 0: Kiểm tra nếu vị trí không âm
        if self.pos_in_path >= 0:
            # pos = path.positions[pos_in_path] 
            # (Lấy tọa độ từ chuỗi đường đi tại vị trí hiện tại)
            pos = self.path.positions[self.pos_in_path]
            
            # rect.center = (round(pos.x), round(pos.y))
            # (Cập nhật vị trí hình chữ nhật để hình ảnh của đối tượng được vẽ đúng nơi)
            self.rect.center = (round(pos.x), round(pos.y))


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_RADIUS)
        if self.bonus is not None:
            screen.blit(pygame.image.load(
                BONUS_IMAGES[self.bonus][self.color]),
                (self.rect.x, self.rect.y))

    def __eq__(self, other):
        return self.color == other.color and \
               self.rect.center == other.rect.center and \
               self.can_move == other.can_move


class ShootingBall(pygame.sprite.Sprite):
    def __init__(self, color, pos=SCREEN_CENTER):
        pygame.sprite.Sprite.__init__(self)

        self.color = color  # Màu sắc của viên đạn

        self.image = pygame.Surface(BALL_SIZE) # Hình ảnh viên đạn
        self.rect = self.image.get_rect(center=pos)   # Vị trí viên đạn

        self.target = (0, 0)  # Mục tiêu và hướng di chuyển của viên đạn
        self.speed = 15  # Tốc độ di chuyển của viên đạn

        self.time = None  # Thời gian tồn tại của viên đạn

    def set_time(self, time):
        self.time = time

    def set_target(self, target):
            # target_vector = (tọa độ x của mục tiêu - tọa độ x của tâm hình chữ nhật (rect.center.x),
        #                  tọa độ y của mục tiêu - tọa độ y của tâm hình chữ nhật (rect.center.y))
        target_vector = (target[0] - self.rect.center[0], 
                        target[1] - self.rect.center[1])
        
        # length = căn bậc hai (target_vector.x^2 + target_vector.y^2)
        length = math.hypot(*target_vector)  # math.hypot = sqrt(x^2 + y^2)
        
        # target = (target_vector.x / length, target_vector.y / length)
        # (chuẩn hóa vector hướng)
        self.target = (target_vector[0] / length, target_vector[1] / length)



    def update(self):
            # Cập nhật vị trí viên đạn dựa trên vận tốc
        self.rect.center = (self.rect.center[0] + self.target[0] * self.speed,
                            self.rect.center[1] + self.target[1] * self.speed)


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_RADIUS)


class Player(pygame.sprite.Sprite):
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)

        if level == 1:
            self.pos = (530, 330)
        else:
            self.pos = SCREEN_CENTER

        self.original_image = pygame.transform.smoothscale(
            pygame.image.load('game/images/player.png'), PLAYER_SIZE)
        self.original_image.set_colorkey(BLACK)

        self.image = self.original_image

        self.rect = self.image.get_rect(center=self.pos)

        self.angle = 0

    def update(self):
        # (mouse_x, mouse_y) = Lấy tọa độ chuột
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # relative_x = mouse_x - vị trí x của hình chữ nhật (rect.x)
        # relative_y = mouse_y - vị trí y của hình chữ nhật (rect.y)
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        # góc (angle) = atan2(-relative_y, relative_x) * (180 / π) + 90
        self.angle = (180 / math.pi) * (-math.atan2(rel_y, rel_x)) + 90
        # hình ảnh (image) = xoay hình ảnh gốc (original_image) theo góc (angle)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.image.set_colorkey(BLACK)
        # hình chữ nhật (rect) = lấy hình chữ nhật bao quanh (get_rect) 
        # của hình ảnh xoay với tâm tại vị trí hiện tại của rect
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Finish(pygame.sprite.Sprite):
    def __init__(self, path, balls, score_manager):
        pygame.sprite.Sprite.__init__(self)

        self.balls = balls
        self.score_manager = score_manager

        self.image = pygame.transform.smoothscale(
            pygame.image.load("game/images/star.png"), (80, 80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=path.positions[-1])

    def update(self): 
#    Lặp qua từng viên bi trong danh sách viên bi (balls):
        for ball in self.balls:
            #  Nếu hình chữ nhật của điểm kết thúc (rect) 
            # va chạm với hình chữ nhật của viên bi (ball.rect):
            if self.rect.colliderect(ball.rect):
                # Gọi hàm thua cuộc (lose()) trong trình quản lý điểm số (score_manager)
                self.score_manager.lose()

    '''Hàm cập nhật (update):
    Lặp qua từng viên bi trong danh sách viên bi (balls):
        Nếu hình chữ nhật của điểm kết thúc (rect) va chạm với hình chữ nhật của viên bi (ball.rect):
            Gọi hàm thua cuộc (lose()) trong trình quản lý điểm số (score_manager)

    '''
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

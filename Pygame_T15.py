import os
import sys
import pygame as pg


# =========================================
# 初期設定
# =========================================

WIDTH = 1000
HEIGHT = 600
FPS = 60

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pg.init()
#ひだ
try:
    pg.mixer.init()
except Exception:
    pass

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

#ひだ ジャンプ音
jump_sound = None
try:
    jump_sound = pg.mixer.Sound(os.path.join('fig', 'jump1.wav'))
except Exception:
    jump_sound = None

# BGM
try:
    pg.mixer.music.load(os.path.join('fig', '追跡者.mp3'))
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(-1)
except Exception:
    pass

# =========================================
# 色
# =========================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
SKY = (135, 206, 235)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)


# =========================================
# Playerクラス
# =========================================

class Player:
    """
    プレイヤーを管理するクラス
    """

    def __init__(self):
        self.x = 200
        self.y = 400

        self.w = 50
        self.h = 50

        self.vy = 0

        self.gravity = 0.8
        self.jump_power = -15

        self.on_ground = True
        #ひだ
        self.image = None
        try:
            self.image = pg.image.load(os.path.join('fig', 'player1.png')).convert_alpha()
        except Exception:
            self.image = None

    def jump(self):
        """
        ジャンプする
        """

        if self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False
            #ひだ ジャンプ音
            if jump_sound:
                jump_sound.play()

    def update(self, ground_y: int):
        """
        プレイヤー更新
        """

        self.vy += self.gravity
        self.y += self.vy

        # 地面判定
        if self.y + self.h >= ground_y:
            self.y = ground_y - self.h
            self.vy = 0
            self.on_ground = True

    def draw(self, screen: pg.Surface):
        """
        プレイヤー描画
        """
    #ひだ
        if self.image:
            img = pg.transform.smoothscale(self.image, (self.w, self.h))
            screen.blit(img, (self.x, self.y))
        else:
            pg.draw.rect(
                screen,
                BLUE,
                (self.x, self.y, self.w, self.h)
            )


# =========================================
# Obstacleクラス
# =========================================

class Obstacle:
    """
    障害物クラス
    """

    def __init__(self):
        self.x = WIDTH
        self.y = 450

        self.w = 50
        self.h = 50

        self.speed = 10
        #ひだ
        self.image = None
        try:
            self.image = pg.image.load(os.path.join('fig', 'shougaibutsu1.png')).convert_alpha()
        except Exception:
            self.image = None

    def update(self):
        """
        障害物更新
        """

        self.x -= self.speed

        # 画面外へ行ったら戻す
        if self.x + self.w < 0:
            self.x = WIDTH + 300

    def draw(self, screen: pg.Surface):
        """
        障害物描画
        """
    #ひだ
        if self.image:
            img = pg.transform.smoothscale(self.image, (self.w, self.h))
            screen.blit(img, (self.x, self.y))
        else:
            pg.draw.rect(
                screen,
                RED,
                (self.x, self.y, self.w, self.h)
            )

    def get_rect(self) -> pg.Rect:
        """
        Rect取得
        """

        return pg.Rect(
            self.x,
            self.y,
            self.w,
            self.h
        )


# =========================================
# Backgroundクラス
# =========================================

class Background:
    """
    背景クラス
    """

    def __init__(self):
        self.scroll_x = 0
        self.scroll_speed = 10
        #ひだ
        self.image = None
        try:
            self.image = pg.image.load(os.path.join('fig', 'background1.png')).convert()
        except Exception:
            self.image = None

    def update(self):
        """
        背景更新
        """

        self.scroll_x -= self.scroll_speed
        #ひだ
        if self.image:
            img_w = self.image.get_width()
            if self.scroll_x <= -img_w:
                self.scroll_x += img_w
        elif self.scroll_x <= -100:
            self.scroll_x = 0

    def draw(self, screen: pg.Surface, ground_y: int):
        """
        背景描画
        """

        #ひだ
        if self.image:
            img_w = self.image.get_width()
            bx = int(self.scroll_x % img_w) - img_w
            while bx < WIDTH:
                screen.blit(self.image, (bx, 0))
                bx += img_w
        else:
            screen.fill(SKY)

        # 地面
        pg.draw.rect(
            screen,
            BLACK,
            (0, ground_y, WIDTH, HEIGHT-ground_y)
        )

        # 地面ライン
        for x in range(0, WIDTH + 100, 100):
            pg.draw.rect(
                screen,
                YELLOW,
                (x + self.scroll_x, ground_y + 40, 50, 10)
            )


# =========================================
# Gameクラス
# =========================================

class Game:
    """
    ゲーム全体クラス
    """

    def __init__(self):

        self.ground_y = 500

        self.player = Player()
        self.obstacle = Obstacle()
        self.background = Background()

        self.font = pg.font.Font(None, 50)
        self.big_font = pg.font.Font(None, 80)

        self.game_over = False

        # スコア
        self.score = 0

        # 距離
        self.distance = 0

    def check_collision(self):
        """
        当たり判定
        """

        player_rect = pg.Rect(
            self.player.x,
            self.player.y,
            self.player.w,
            self.player.h
        )

        obstacle_rect = self.obstacle.get_rect()

        if player_rect.colliderect(obstacle_rect):
            self.game_over = True

    def update(self):
        """
        更新処理
        """

        if not self.game_over:

            self.player.update(self.ground_y)
            self.obstacle.update()
            self.background.update()

            self.check_collision()

            # スコア加算
            self.score += 0.1

            # 距離加算
            self.distance += self.obstacle.speed

    def draw(self, screen: pg.Surface):
        """
        描画処理
        """

        self.background.draw(screen, self.ground_y)

        self.player.draw(screen)
        self.obstacle.draw(screen)

        # SCORE表示
        score_text = self.font.render(
            f"SCORE : {int(self.score)}",
            True,
            BLACK
        )

        screen.blit(score_text, (20, 20))

        # GAME OVER画面
        if self.game_over:

            # 半透明背景
            overlay = pg.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)

            screen.blit(overlay, (0, 0))

            # GAME OVER
            gameover_text = self.big_font.render(
                "GAME OVER",
                True,
                WHITE
            )

            gameover_rect = gameover_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 80)
            )

            screen.blit(gameover_text, gameover_rect)

            # DISTANCE表示
            result_distance = self.font.render(
                f"DISTANCE : {int(self.distance)} m",
                True,
                WHITE
            )

            distance_rect = result_distance.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 20)
            )

            screen.blit(result_distance, distance_rect)


# =========================================
# メイン関数
# =========================================

def main():
    """
    メイン関数
    """

    game = Game()

    running = True

    while running:

        clock.tick(FPS)

        # イベント処理
        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_SPACE:
                    game.player.jump()

        # 更新
        game.update()

        # 描画
        game.draw(screen)

        pg.display.update()

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
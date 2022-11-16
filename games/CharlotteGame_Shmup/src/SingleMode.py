import pygame

from os import path
from mlgame.game.paia_game import GameResultState, GameStatus
from mlgame.utils.enum import get_ai_name

from game_module.TiledMap import create_construction
from .Player import Player
from .Mob import Mob

SCENE_WIDTH = 1000
SCENE_HEIGHT = 800


class SingleMode:
    def __init__(self, play_rect_area: pygame.Rect):
        pygame.init()
        self._user_num = 1
        self.scene_width = SCENE_WIDTH
        self.scene_height = SCENE_HEIGHT
        self.play_rect_area = play_rect_area
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.player = Player(create_construction(get_ai_name(0), 0, (0, 0), (50, 50)))

        self.used_frame = 0
        self.state = GameResultState.FAIL
        self.status = GameStatus.GAME_ALIVE
        self.width_center = SCENE_WIDTH // 2
        self.height_center = SCENE_HEIGHT // 2
        x = 5
        for i in range(x):
            mob = Mob(create_construction(get_ai_name(0), 0, (i*10, i*10), (50, 50)))
            self.mobs.add(mob)
        self.all_sprites.add(self.player, self.mobs)

    def update(self, command: dict) -> None:
        self.used_frame += 1
        self.player.update(command)
        self.mobs.update(command)
        if not self.player.get_is_alive():
            self.get_player_end()

    def reset(self) -> None:
        self.__init__(self.play_rect_area)

    def get_player_end(self):
        self.set_result(GameResultState.FINISH, GameStatus.GAME_OVER)

    def set_result(self, state: str, status: str):
        self.state = state
        self.status = status

    def get_player_result(self) -> list:
        """Define the end of game will return the player's info for user"""
        res = []
        get_res = self.player.get_info_to_game_result()
        get_res["state"] = self.state
        get_res["status"] = self.status
        get_res["used_frame"] = self.used_frame
        res.append(get_res)
        return res

    def check_collisions(self):
        raise Exception("Please overwrite check_collisions")

    def get_init_image_data(self) -> list:
        init_image_data = [self.player.get_obj_init_data()]
        for mob in self.mobs:
            if isinstance(mob, Mob):
                init_image_data.append(mob.get_obj_init_data())
                break

        return init_image_data

    def get_ai_data_to_player(self):
        to_player_data = self.player.get_data_from_obj_to_game()
        to_player_data["used_frame"] = self.used_frame
        to_player_data["status"] = self.status
        to_player_data["player_info"] = [self.player.get_data_from_obj_to_game()]

        return {get_ai_name(0): to_player_data}

    def get_background_view_data(self) -> list:
        background_view_data = []
        return background_view_data

    def get_obj_progress_data(self) -> list:
        # obj_progress_data = [self.draw_player(), self.all_sprites.get_obj_progress_data()]
        obj_progress_data = []
        for i in self.all_sprites:
            obj_progress_data.append(i.get_obj_progress_data())
        return obj_progress_data

    def get_bias_toggle_progress_data(self) -> list:
        bias_toggle_progress_data = []
        return bias_toggle_progress_data

    def get_toggle_progress_data(self) -> list:
        toggle_data = []
        return toggle_data

    def get_foreground_progress_data(self) -> list:
        foreground_data = []
        return foreground_data

    def get_user_info_data(self) -> list:
        user_info_data = []
        return user_info_data

    def get_game_sys_info_data(self) -> dict:
        game_sys_info_data = {}
        return game_sys_info_data

    def draw_player(self) -> list:
        player_data = self.player.get_obj_progress_data()

        return player_data

    def debugging(self, is_debug: bool) -> list:
        if is_debug:
            raise Exception("Please over writing debugging")
        return []

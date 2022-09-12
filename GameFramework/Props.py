import pygame
from mlgame.view.view_model import create_rect_view_data, create_asset_init_data

vec = pygame.math.Vector2


class Props(pygame.sprite.Sprite):
    def __init__(self, construction: dict, **kwargs):
        """
        初始化物件資料
        construction可直接由TiledMap打包地圖資訊後傳入
        :param construction:
        :param kwargs:
        """
        super().__init__()
        self._id = construction["_id"]
        self._no = construction["_no"]
        self.rect = pygame.Rect(construction["_init_pos"], construction["_init_size"])
        self._color = "#ffffff"
        self._origin_xy = self.rect.topleft
        self._origin_center = self.rect.center
        self._angle = 0
        self._used_frame = 0
        self._shield = 100
        self._lives = 3
        self._vel = vec(0, 0)
        self._is_alive = True

    def update(self, *args, **kwargs) -> None:
        """
        更新物件資料
        :param args:
        :param kwargs:
        :return:
        """
        raise Exception("Please overwrite update")

    def reset(self) -> None:
        """
        Reset Prop pos = origin_pos
        :return:
        """
        self.rect.topleft = self._origin_xy

    def reset_xy(self, new_pos: tuple) -> None:
        """
        :param new_pos:
        :return:
        """
        self.rect.topleft = new_pos

    def get_xy(self) -> tuple:
        """
        :return: topleft
        """
        return self.rect.topleft

    def get_size(self) -> tuple:
        """
        :return: width, height
        """
        return self.rect.width, self.rect.height

    def get_center(self) -> tuple:
        """
        :return: center
        """
        return self.rect.center

    def get_lives(self) -> int:
        """
        :return: _lives
        """
        return self._lives

    def get_shield(self) -> int:
        """
        :return: _shield
        """
        return self._shield

    def get_is_alive(self) -> bool:
        """
        :return: _is_alive
        """
        return self._is_alive

    def get_data_from_obj_to_game(self) -> dict:
        """
        在遊戲主程式獲取遊戲資料給AI時被調用
        return {
            "x": self.rect.x,
            "y": self.rect.y
            }
        :return:
        """
        info = {"id": f"{self._id}"
                , "x": self.rect.x
                , "y": self.rect.y
                }
        return info

    def get_obj_progress_data(self) -> dict or list:
        """
        使用view_model函式，建立符合mlgame物件更新資料格式的資料，在遊戲主程式更新畫面資訊時被調用
        :return:
        """
        obj_data = create_rect_view_data(f"{self._id}"
                                         , *self.rect.topleft
                                         , self.rect.width
                                         , self.rect.height
                                         , self._color
                                         , self._angle)
        return obj_data

    def get_obj_init_data(self) -> dict or list:
        """
        使用view_model函式，建立符合mlgame物件初始資料格式的資料，在遊戲主程式初始畫面資訊時被調用
        :return:
        """
        image_init_data = create_asset_init_data(f"{self._id}", self.rect.width, self.rect.height, "image_full_name", "url")
        return image_init_data


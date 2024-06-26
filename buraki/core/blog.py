"""
Бизнес-модели блога.

@toc
    * [public class Category](#public-class-category)

@author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
@copyright Copyright (c) 2024-present Rasim Eminov
@license MIT
@since 0.1.0
"""

import enum

__all__ = (
    "Category",
)


@enum.unique
class Category(enum.StrEnum):
    """
    Перечисление категорий постов в блоге.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @since 0.1.0
    """

    IT = "IT"
    BUSINESS = "Бизнес"
    SPORT = "Спорт"

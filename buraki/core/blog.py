"""
Бизнес-модели блога.

@toc
    * [public class Category](#public-class-category)
    * [public class Post](#public-class-post)

@author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
@copyright Copyright (c) 2024-present Rasim Eminov
@license MIT
@since 0.1.0
"""

import datetime
import enum
import uuid
from typing import List

__all__ = (
    "Category",
    "Post"
)


@enum.unique
class Category(enum.StrEnum):
    """
    Перечисление категорий постов в блоге.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @see buraki.core.blog.Post
    @since 0.1.0
    """

    IT = "IT"
    BUSINESS = "Бизнес"
    SPORT = "Спорт"


class Post:
    """
    Бизнес-модель поста в блоге.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @see buraki.core.blog.Category
    @since 0.1.0
    """

    __slots__ = (
        "_post_id",
        "_category",
        "_created_at",
        "_topic",
        "_content",
        "_tags",
        "_likes",
        "_dislikes"
    )

    def __init__(
        self,
        post_id: uuid.UUID,
        category: Category,
        created_at: datetime.datetime,
        topic: str,
        content: str,
        tags: List[str],
        likes: int,
        dislikes: int
    ):
        """
        Конструктор бизнес-модели поста в блоге.

        @parameter post_id
            Идентификатор поста.
        @ptype post_id
            uuid.UUID
        @parameter category
            Категория поста.
        @ptype category
            buraki.core.blog.Category
        @parameter created_at
            Дата и время публикации поста.
        @ptype created_at
            datetime.datetime
        @parameter topic
            Заголовок поста.
        @ptype topic
            str
        @parameter content
            Содержимое поста: текст, медиа, файлы и прочее.
        @ptype content
            str
        @parameter tags
            Теги поста.
        @ptype tags
            typing.List[str]
        @parameter likes
            Число отметок "Нравится" у поста.
        @ptype likes
            int
        @parameter dislikes
            Число отметок "Не нравится" у поста.
        @ptype dislikes
            int
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.blog.Category
        @since 0.1.0
        """
        self._post_id = post_id
        self._category = category
        self._created_at = created_at
        self._topic = topic
        self._content = content
        self._tags = tags
        self._likes = likes
        self._dislikes = dislikes

    @property
    def post_id(self) -> uuid.UUID:
        return self._post_id

    def __eq__(self, other):
        return (
            self is other or (
                isinstance(other, Post) and
                self._post_id == other._post_id
            )
        )

    def __repr__(self):
        return (
            f"{type(self).__qualname__}("
            f"post_id={self._post_id!r}, "
            f"category={self._category!r}, "
            f"created_at={self._created_at!r}, "
            f"topic={self._topic!r}, "
            f"content={self._content!r}, "
            f"tags={self._tags!r}, "
            f"likes={self._likes!r}, "
            f"dislikes={self._dislikes!r})"
        )

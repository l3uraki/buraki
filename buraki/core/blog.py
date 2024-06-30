"""
Бизнес-модели блога.

@toc
    * [public class Category](#public-class-category)
    * [public class Post](#public-class-post)
    * [public class PostCategorySpecification](#public-class-postcategoryspecification)
    * [public class PostCreatedAtSpecification](#public-class-postcreatedatspecification)

@author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
@copyright Copyright (c) 2024-present Rasim Eminov
@license MIT
@since 0.1.0
"""

import datetime
import enum
import typing
import uuid
from typing import List, Tuple

import buraki.core.common as core_common

__all__ = (
    "Category",
    "Post",
    "PostCategorySpecification",
    "PostCreatedAtSpecification"
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

    @property
    def category(self) -> Category:
        return self._category

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

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


class PostCategorySpecification(core_common.CompositeSpecification[Post]):
    """
    Спецификация категории поста в блоге.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @see buraki.core.blog.Category
    @see buraki.core.blog.Post
    @see buraki.core.common.CompositeSpecification
    @since 0.1.0
    """

    __slots__ = "_reference_category"

    def __init__(self, reference_category: Category):
        """
        Конструктор спецификации категории поста в блоге.

        @parameter reference_category
            Эталонная категория поста.
        @ptype reference_category
            buraki.core.blog.Category
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @see buraki.core.blog.Category
        @since 0.1.0
        """
        self._reference_category = reference_category

    @typing.override
    def get_filters(self) -> Tuple:
        return (
            self._reference_category,
        )

    @typing.override
    def is_satisfied_by(self, candidate: Post) -> bool:
        return candidate.category == self._reference_category


class PostCreatedAtSpecification(core_common.CompositeSpecification[Post]):
    """
    Спецификация даты и времени публикации поста в блоге.

    @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
    @see buraki.core.blog.Post
    @see buraki.core.common.CompositeSpecification
    @since 0.1.0
    """

    __slots__ = (
        "_created_from",
        "_created_to"
    )

    def __init__(self, created_from: datetime.datetime, created_to: datetime.datetime):
        """
        Конструктор спецификации даты и времени публикации поста в
        блоге.

        @parameter created_from
            Нижняя граница даты и времени публикации поста.
        @ptype created_from
            datetime.datetime
        @parameter created_to
            Верхняя граница даты и времени публикации поста.
        @ptype created_to
            datetime.datetime
        @author Расим "Buraki" Эминов <eminov.workspace@yandex.ru>
        @since 0.1.0
        """
        self._created_from = created_from
        self._created_to = created_to

    @typing.override
    def get_filters(self) -> Tuple:
        return (
            self._created_from,
            self._created_to
        )

    @typing.override
    def is_satisfied_by(self, candidate: Post) -> bool:
        return self._created_from <= candidate.created_at <= self._created_to

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(80), nullable=False)
    lastname: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    # password: Mapped[str] = mapped_column(nullable=False)
    # is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    post: Mapped[List["Posts"]] = relationship(back_populates="user_post")

    comment_user: Mapped[List["Comments"]] = relationship(back_populates="user_comment")

    followers: Mapped[List["Followers"]] = relationship(back_populates="user_to", foreign_keys="[Followers.user_to_id]")
    following: Mapped[List["Followers"]] = relationship(back_populates="user_from", foreign_keys="[Followers.user_from_id]")


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "post": [post.serialize() for post in self.post],
            "comment_user": [comment.serialize() for comment in self.comment_user],
            "followers": [follower.serialize() for follower in self.followers],
            "following": [followed.serialize() for followed in self.following],
        }
    
class Posts(db.Model):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    body: Mapped[str] = mapped_column(String(500), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_post: Mapped["Users"] = relationship(back_populates="post")

    comment_post: Mapped[List["Comments"]] = relationship(back_populates="post")

    media_post: Mapped["Medias"] = relationship(back_populates="post_media")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "user_post": self.user_post.username,
            "comment_post": [comment.serialize() for comment in self.comment_post],
            "media_post": self.media_post.serialize()
            
        }

class Comments(db.Model):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(String(200), nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Posts"] = relationship(back_populates="comment_post")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_comment: Mapped["Users"] = relationship(back_populates="comment_user")


    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "post": self.post.title,
            "user_comment": self.user_comment.username
        }
    

class Medias(db.Model):
    __tablename__ = 'medias'
    id: Mapped[int] = mapped_column(primary_key=True)
    types: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(80), nullable=False)
    
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post_media: Mapped["Posts"] = relationship(back_populates="media_post")

    def serialize(self):
        return {
            "id": self.id,
            "types": self.types,
            "url": self.url,
            "post_media": self.post_media.serialize()
        }
    
class Followers(db.Model):
    __tablename__ = 'followers'
    user_to_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    date: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)

    user_to: Mapped["Users"] = relationship(back_populates="followers", foreign_keys=[user_to_id])
    user_from: Mapped["Users"] = relationship(back_populates="following", foreign_keys=[user_from_id])

    def serialize(self):
        return {
            "user_to_id": self.user_to_id,
            "user_from_id": self.user_from_id,
            "date": self.date.isoformat()
        }
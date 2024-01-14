#!/usr/bin/python3
"""This module creates a Review class"""
from models.base_model import BaseModel


class Review(BaseModel):
""" state class inherits from BaseModel """

place_id = ""
user_id = ""
text = ""


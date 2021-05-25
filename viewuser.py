from flask import Flask,session,redirect,url_for, Blueprint
from pymongo import MongoClient

view=Blueprint("view",__name__)


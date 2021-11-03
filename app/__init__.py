# Kazimierz Major -- Andrew Juang, Noakai Aronesty, Eric Guo, Qina Liu
# SoftDev
# P00 -- Web Log Hosting Site

from os import urandom
from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3, os.path

app = Flask(__name__)

app.secret_key = urandom(32)

from app import views
from app import auth

import os
# import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def message(message):
    """Render a message to the user"""
    return render_template("message_page.html", message=message)
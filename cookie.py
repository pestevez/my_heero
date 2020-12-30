""" Class to store the Eero API Cookie, which is required by the Client """
import eero

class CookieStore(eero.SessionStorage):
  def  __init__(self, user_token):
    self.user_token = user_token

  @property
  def cookie(self):
    return self.user_token

  @cookie.setter
  def cookie(self, cookie):
    self.user_token = cookie

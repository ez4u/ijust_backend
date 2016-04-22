# -*- coding: utf-8 -*-

from good import Schema, All, Required, Length, Match, Email


login_schema = Schema({
						Required('login'): unicode,
						Required('password'): unicode
					   })


signup_schema = Schema({
						Required('username'): All(unicode, Match(r'^[\w.]+$'), Length(max=32)),
						Required('email'): Email(),
						Required('password'): All(unicode, Length(max=32))
					   })

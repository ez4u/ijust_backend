# -*- coding: utf-8 -*-

from good import Schema, All, Required, Optional, Length, Match, Email


login_schema = Schema({
						Required('login'): unicode,
						Required('password'): unicode
					   })


signup_schema = Schema({
						Required('username'): All(unicode, Match(r'^[\w.]+$'), Length(max=32)),
						Required('email'): Email(),
						Required('password'): All(unicode, Length(min=3, max=32))
					   })


edit_schema = Schema({
						Optional('firstname'): All(unicode, Length(max=32)),
						Optional('lastname'): All(unicode, Length(max=32)),
						Optional('password'): Schema({
														Required('old'): All(unicode, Length(min=3, max=32)),
														Required('new'): All(unicode, Length(min=3, max=32))
													 })
					   })

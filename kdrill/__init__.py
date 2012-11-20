# -*- coding: utf-8 -*-
#
# kdrill - Anki plugin to (un)suspend cards according to KDrill usefile
#
# Copyright (c) 2010  Frédéric Brière <fbriere@fbriere.net>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.


from ankiqt import mw
from kdrill.main import init

# (What is the id paramter for?)
mw.registerPlugin("KDrill", 0)
mw.addHook("init", init)

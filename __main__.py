# ad2template - A Python script that generates files from Jinja2 templates
# using attributes from Active Directory (AD).
# Copyright (C) 2024 Tobias Wintrich
#
# This file is part of ad2template.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from ad2template import ad2template

if __name__ == '__main__':
    ad2template = ad2template()
    ad2template.writeTemplates()


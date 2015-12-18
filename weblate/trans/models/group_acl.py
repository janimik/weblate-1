# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2015 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
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
#

"""Whiteboard model."""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import Group
from weblate.lang.models import Language

class GroupACL(models.Model):

    groups = models.ManyToManyField(Group)

    # avoid importing Project and SubProject because of circular dependency
    project = models.ForeignKey('Project', null=True, blank=True)
    subproject = models.ForeignKey('SubProject', null=True, blank=True)
    language = models.ForeignKey(Language, null=True, blank=True)

    def clean(self):
        if not self.project and not self.subproject and not self.language:
            raise ValidationError(_('Project, subproject or language must be specified'))

        # specify either language or project/subproject
        # This restriction is arbitrary, in order to prevent confusing configurations.
        # But maybe we should simply allow that?
        if self.language and (self.project or self.subproject):
            raise ValidationError(_('Either language or project/subproject can be specified, but not both'))

        # ignore project if subproject is set
        if self.project and self.subproject:
            self.project = None

    class Meta(object):
        unique_together = ('project', 'subproject', 'language')
        verbose_name = _('Group ACL')
        verbose_name_plural = _('Group ACLs')

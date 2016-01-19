# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables
from horizon.utils import filters

from senlin_dashboard import api


class CreateNode(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Node")
    url = "horizon:cluster:nodes:create"
    classes = ("ajax-modal", "btn-create")
    icon = "plus"
    ajax = True


class DeleteNode(tables.DeleteAction):

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Node",
            u"Delete Nodes",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Node",
            u"Deleted Nodes",
            count
        )

    def delete(self, request, obj_id):
        api.senlin.node_delete(request, obj_id)


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, node_id):
        node = api.senlin.node_get(request, node_id)
        return node


def get_profile_link(node):
    return reverse_lazy('horizon:cluster:profiles:detail',
                        args=[node.profile_id])


def get_physical_link(node):
    if node.physical_id:
        return reverse_lazy('horizon:project:instances:detail',
                            args=[node.physical_id])


def get_updated_time(object):
    return filters.parse_isotime(object.updated_at) or None


class NodesTable(tables.DataTable):
    STATUS_CHOICES = (
        ("INIT", None),
        ("ACTIVE", True),
        ("ERROR", False),
        ("DELETED", False),
        ("WARNING", None),
        ("CREATING", None),
        ("UPDATING", None),
        ("DELETING", None),
    )

    STATUS_DISPLAY_CHOICES = (
        ("INIT", pgettext_lazy("Current status of a Node", u"INIT")),
        ("ACTIVE", pgettext_lazy("Current status of a Node", u"ACTIVE")),
        ("ERROR", pgettext_lazy("Current status of a Node", u"ERROR")),
        ("DELETED", pgettext_lazy("Current status of a Node", u"DELETED")),
        ("WARNING", pgettext_lazy("Current status of a Node", u"WARNING")),
        ("CREATING", pgettext_lazy("Current status of a Node", u"CREATING")),
        ("UPDATING", pgettext_lazy("Current status of a Node", u"UPDATING")),
        ("DELETING", pgettext_lazy("Current status of a Node", u"DELETING")),
    )

    name = tables.Column("name", verbose_name=_("Name"),
                         link="horizon:cluster:nodes:detail")
    profile_name = tables.Column("profile_name",
                                 link=get_profile_link,
                                 verbose_name=_("Profile Name"))
    physical_id = tables.Column("physical_id",
                                link=get_physical_link,
                                verbose_name=_("Physical ID"))
    role = tables.Column("role", verbose_name=_("Role"))
    status = tables.Column("status",
                           verbose_name=_("Status"),
                           status=True,
                           status_choices=STATUS_CHOICES,
                           display_choices=STATUS_DISPLAY_CHOICES)
    status_reason = tables.Column("status_reason",
                                  verbose_name=_("Status Reason"))
    created = tables.Column(
        "created_at",
        verbose_name=_("Created"),
        filters=(
            filters.parse_isotime,
        )
    )
    updated = tables.Column(
        get_updated_time,
        verbose_name=_("Updated"),
    )

    class Meta(object):
        name = "nodes"
        row_class = UpdateRow
        verbose_name = _("Nodes")
        status_columns = ["status"]
        table_actions = (tables.FilterAction,
                         CreateNode,
                         DeleteNode,)
        row_actions = (DeleteNode,)

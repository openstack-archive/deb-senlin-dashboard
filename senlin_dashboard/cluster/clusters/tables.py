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


class CreateCluster(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Cluster")
    url = "horizon:cluster:clusters:create"
    classes = ("ajax-modal", "btn-create")
    icon = "plus"
    ajax = True


def get_profile_link(cluster):
    return reverse_lazy('horizon:cluster:profiles:detail',
                        args=[cluster.profile_id])


def get_updated_time(object):
    return filters.parse_isotime(object.updated_at) or None


class DeleteCluster(tables.DeleteAction):

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Cluster",
            u"Delete Clusters",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Cluster",
            u"Deleted Clusters",
            count
        )

    def delete(self, request, obj_id):
        api.senlin.cluster_delete(request, obj_id)


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request, cluster_id):
        cluster = api.senlin.cluster_get(request, cluster_id)
        return cluster


class ClustersTable(tables.DataTable):
    STATUS_CHOICES = (
        ("INIT", None),
        ("ACTIVE", True),
        ("ERROR", False),
        ("DELETED", False),
        ("CRITICAL", False),
        ("WARNING", None),
        ("CREATING", None),
        ("UPDATING", None),
        ("DELETING", None),
    )

    STATUS_DISPLAY_CHOICES = (
        ("INIT", pgettext_lazy("Current status of a Cluster", u"INIT")),
        ("ACTIVE", pgettext_lazy("Current status of a Cluster", u"ACTIVE")),
        ("ERROR", pgettext_lazy("Current status of a Cluster", u"ERROR")),
        ("DELETED", pgettext_lazy("Current status of a Cluster", u"DELETED")),
        ("CRITICAL", pgettext_lazy("Current status of a Cluster",
                                   u"CRITICAL")),
        ("WARNING", pgettext_lazy("Current status of a Cluster", u"WARNING")),
        ("CREATING", pgettext_lazy("Current status of a Cluster",
                                   u"CREATING")),
        ("UPDATING", pgettext_lazy("Current status of a Cluster",
                                   u"UPDATING")),
        ("DELETING", pgettext_lazy("Current status of a Cluster",
                                   u"DELETING")),
    )

    name = tables.Column("name", verbose_name=_("Name"),
                         link="horizon:cluster:clusters:detail")
    status = tables.Column("status",
                           verbose_name=_("Status"),
                           status=True,
                           status_choices=STATUS_CHOICES,
                           display_choices=STATUS_DISPLAY_CHOICES)
    status_reason = tables.Column("status_reason",
                                  verbose_name=_("Status Reason"))
    profile_name = tables.Column("profile_name",
                                 link=get_profile_link,
                                 verbose_name=_("Profile Name"))
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
        name = "clusters"
        row_class = UpdateRow
        verbose_name = _("Clusters")
        status_columns = ["status"]
        table_actions = (tables.FilterAction,
                         CreateCluster,
                         DeleteCluster,)
        row_actions = (DeleteCluster,)

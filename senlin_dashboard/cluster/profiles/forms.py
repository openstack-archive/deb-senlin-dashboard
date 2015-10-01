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

"""
Views for managing profiles.
"""

import six
import yaml

from senlinclient.common import utils

from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from senlin_dashboard.api import senlin

INDEX_URL = "horizon:cluster:profiles:index"
CREATE_URL = "horizon:cluster:profiles:create"
UPDATE_URL = "horizon:cluster:profiles:update"
DETAIL_URL = "horizon:cluster:profiles:detail"


def _populate_profile_params(name, spec, permission, metadata, id=None):

    if spec is None:
        spec_dict = None
    else:
        try:
            spec_dict = yaml.load(spec)
        except Exception as ex:
            raise ValidationError(_('The specified file is not a valid '
                                    'YAML file: %s') % six.text_type(ex))
        type_name = spec_dict['type']
        if type_name == 'os.heat.stack':
            spec_dict['properties'] = utils.process_stack_spec(
                spec['properties'])
    if not metadata:
        metadata_dict = {}
    else:
        try:
            metadata_dict = yaml.load(metadata)
        except Exception as ex:
            raise ValidationError(_('The specified file is not a valid '
                                    'YAML file: %s') % six.text_type(ex))
    params = {"name": name,
              "spec": spec_dict,
              "permission": permission,
              "metadata": metadata_dict}

    if id is not None:
        params["id"] = id

    return params


class CreateProfileForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255, label=_("Name"))
    source_type = forms.ChoiceField(
        label=_('Spec Source'),
        required=False,
        choices=[('file', _('File')),
                 ('yaml', _('YAML'))],
        widget=forms.Select(attrs={
            'class': 'switchable',
            'data-slug': 'source'}))
    spec_file = forms.FileField(label=_("Spec File"),
                                widget=forms.FileInput(attrs={
                                    'class': 'switched',
                                    'data-switch-on': 'source',
                                    'data-source-file': _('Spec File')}),
                                required=False)
    spec_yaml = forms.CharField(max_length=255,
                                label=_("Spec YAML"),
                                widget=forms.Textarea(attrs={
                                    'rows': 6,
                                    'class': 'switched',
                                    'data-switch-on': 'source',
                                    'data-source-yaml': _('Spec YAML')}),
                                required=False)
    permission = forms.CharField(max_length=255,
                                 label=_("Permission"),
                                 required=False)
    metadata = forms.CharField(max_length=255,
                               label=_("Metadata"),
                               required=False,
                               widget=forms.Textarea(attrs={'rows': 4}))

    def handle(self, request, data):
        source_type = data.get('source_type')
        if source_type == "yaml":
            spec = data.get("spec_yaml")
        else:
            spec = self.files['spec_file'].read()
        opts = _populate_profile_params(
            name=data.get('name'),
            spec=spec,
            permission=data.get('permission'),
            metadata=data.get('metadata')
        )

        try:
            profile = senlin.profile_create(request, opts)
            messages.success(request,
                             _('Your profile %s has been created.') %
                             opts['name'])
            return profile
        except ValidationError as e:
            self.api_error(e.messages[0])
            return False
        except Exception:
            redirect = reverse(INDEX_URL)
            msg = _('Unable to create new profile')
            exceptions.handle(request, msg, redirect=redirect)
            return False


class UpdateProfileForm(forms.SelfHandlingForm):
    profile_id = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=255, label=_("Name"))
    type = forms.CharField(
        label=_('Type'),
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    spec = forms.CharField(max_length=255,
                           label=_("Spec"),
                           widget=forms.Textarea(attrs={'rows': 6,
                                                 'readonly': 'readonly'}))
    permission = forms.CharField(max_length=255,
                                 label=_("Permission"),
                                 required=False)
    metadata = forms.CharField(max_length=255,
                               label=_("Metadata"),
                               required=False,
                               widget=forms.Textarea(attrs={'rows': 4}))

    def handle(self, request, data):
        opts = _populate_profile_params(
            id=data.get('profile_id'),
            name=data.get('name'),
            spec=None,
            permission=data.get('permission', ''),
            metadata=data.get('metadata', {})
        )

        try:
            senlin.profile_update(request, opts)
            messages.success(request,
                             _('Your profile %s has been updated.') %
                             opts['name'])
            return True
        except ValidationError as e:
            self.api_error(e.messages[0])
            return False
        except Exception:
            redirect = reverse(INDEX_URL)
            msg = _('Unable to update profile')
            exceptions.handle(request, msg, redirect=redirect)
            return False

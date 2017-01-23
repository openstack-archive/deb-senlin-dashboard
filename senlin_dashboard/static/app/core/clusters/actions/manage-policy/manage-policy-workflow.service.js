/*
 *    (c) Copyright 2015 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the 'License');
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function () {
  'use strict';

  angular
    .module('horizon.cluster.clusters.actions')
    .factory('horizon.cluster.clusters.actions.manage-policy.service.workflow',
      managePolicyWorkflow);

  managePolicyWorkflow.$inject = [
    'horizon.app.core.clusters.basePath',
    'horizon.app.core.workflow.factory',
    'horizon.framework.util.i18n.gettext'
  ];

  function managePolicyWorkflow(basePath, workflowService, gettext) {
    return workflowService({
      title: gettext('Manage Policies'),
      steps: [
        {
          id: 'managepolicies',
          title: gettext('Policies'),
          templateUrl: basePath + 'actions/manage-policy/manage-policy.html',
          helpUrl: basePath + 'actions/manage-policy/manage-policy.help.html',
          formName: 'managePoliciesForm'
        }
      ],
      btnText: {
        finish: gettext('Manage Policies')
      },
      btnIcon: {
        finish: 'fa fa-check'
      }
    });
  }
})();

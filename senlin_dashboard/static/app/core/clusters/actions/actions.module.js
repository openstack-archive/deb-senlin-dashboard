/*
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function() {
  'use strict';

  /**
   * @ngdoc overview
   * @ngname horizon.cluster.clusters.actions
   *
   * @description
   * Provides all of the actions for clusters.
   */
  angular.module('horizon.cluster.clusters.actions', [
    'horizon.framework.conf',
    'horizon.cluster.clusters'
  ])
    .run(registerClusterActions);

  registerClusterActions.$inject = [
    'horizon.framework.conf.resource-type-registry.service',
    'horizon.cluster.clusters.actions.create.service',
    'horizon.cluster.clusters.actions.manage-policy.service',
    'horizon.app.core.clusters.resourceType'
  ];

  function registerClusterActions(
    registry,
    createClusterService,
    managePolicyService,
    clusterResourceType
  ) {
    var resourceType = registry.getResourceType(clusterResourceType);

    resourceType.globalActions
      .append({
        id: 'createClusterAction',
        service: createClusterService,
        template: {
          text: gettext('Create Cluster'),
          type: 'create'
        }
      });

    resourceType.itemActions
      .append({
        id: 'managePolicyAction',
        service: managePolicyService,
        template: {
          text: gettext('Manage Policies')
        }
      });
  }

})();

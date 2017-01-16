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
   * @ngname horizon.cluster.receivers.details
   *
   * @description
   * Provides details features for senlin receiver.
   */
  angular.module('horizon.cluster.receivers.details', [
    'horizon.framework.conf',
    'horizon.app.core'
  ])
   .run(registerReceiverDetails);

  registerReceiverDetails.$inject = [
    'horizon.app.core.receivers.basePath',
    'horizon.app.core.receivers.resourceType',
    'horizon.cluster.receivers.service',
    'horizon.framework.conf.resource-type-registry.service'
  ];

  function registerReceiverDetails(
    basePath,
    receiverResourceType,
    receiverService,
    registry
  ) {
    registry.getResourceType(receiverResourceType)
      .setLoadFunction(receiverService.getReceiverPromise)
      .detailsViews
      .append({
        id: 'receiverDetailsOverview',
        name: gettext('Overview'),
        template: basePath + 'details/overview.html'
      });
  }
})();

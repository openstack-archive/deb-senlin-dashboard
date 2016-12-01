/**
 * Copyright 2016 NEC Corporation
 *
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
   * @ngdoc factory
   * @name horizon.cluster.profiles.actions.create.service
   * @description
   * Service for the cluster profile create modal
   */
  angular
    .module('horizon.cluster.profiles.actions')
    .factory('horizon.cluster.profiles.actions.create.service', createService);

  createService.$inject = [
    '$location',
    'horizon.app.core.openstack-service-api.policy',
    'horizon.framework.util.actions.action-result.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.framework.util.q.extensions',
    'horizon.framework.widgets.modal.wizard-modal.service',
    'horizon.framework.widgets.toast.service',
    'horizon.cluster.profiles.actions.create.model',
    'horizon.app.core.profiles.resourceType',
    'horizon.cluster.profiles.actions.create.service.workflow'
  ];

  function createService(
    $location, policy, actionResult, gettext, $qExtensions, wizardModalService, toast,
    model, resourceType, createWorkflow
  ) {

    var scope;
    var message = {
      success: gettext('Profile %s was successfully created.')
    };

    var service = {
      initScope: initScope,
      perform: perform,
      allowed: allowed
    };

    return service;

    //////////////

    function initScope($scope) {
      scope = $scope;
      scope.workflow = createWorkflow;
      scope.model = model;
      scope.$on('$destroy', function() {
      });
    }

    function perform(selected) {
      scope.model.init();
      scope.selected = selected;
      return wizardModalService.modal({
        scope: scope,
        workflow: createWorkflow,
        submit: submit
      }).result;
    }

    function allowed() {
      return $qExtensions.booleanAsPromise(true);
    }

    function submit() {
      return model.createProfile().then(success, true);
    }

    function success(response) {
      toast.add('success', interpolate(message.success, [response.data.id]));
      var result = actionResult.getActionResult()
                   .created(resourceType, response.data.id);
      if (result.result.failed.length === 0 && result.result.created.length > 0) {
        $location.path("/cluster/profiles");
      } else {
        return result.result;
      }
    }
  }
})();

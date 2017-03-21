/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function() {
  "use strict";

  angular
    .module('horizon.cluster.receivers')
    .factory('horizon.cluster.receivers.service', receiversService);

  receiversService.$inject = [
    'horizon.app.core.detailRoute',
    'horizon.app.core.openstack-service-api.senlin'
  ];

  /*
   * @ngdoc factory
   * @name horizon.cluster.receivers.service
   *
   * @description
   * This service provides functions that are used through
   * the Receivers features.
   */
  function receiversService(detailRoute, senlin) {
    return {
      getDetailsPath: getDetailsPath,
      getReceiverPromise: getReceiverPromise,
      getReceiversPromise: getReceiversPromise
    };

    /*
     * @ngdoc function
     * @name getDetailsPath
     * @param item {Object} - The receiver object
     * @description
     * Returns the relative path to the details view.
     */
    function getDetailsPath(item) {
      return detailRoute + 'OS::Senlin::Receiver/' + item.id;
    }

    /*
     * @ngdoc function
     * @name getReceiverPromise
     * @description
     * Given an id, returns a promise for the receiver data.
     */
    function getReceiverPromise(identifier) {
      return senlin.getReceiver(identifier);
    }

    /*
     * @ngdoc function
     * @name getReceiversPromise
     * @description
     * Given filter/query parameters, returns a promise for the matching
     * receivers.  This is used in displaying lists of Receivers.
     */
    function getReceiversPromise(params) {
      return senlin.getReceivers(params).then(modifyResponse);
    }

    function modifyResponse(response) {
      return {data: {items: response.data.items.map(modifyItem)}};

      function modifyItem(item) {
        var timestamp = item.updated_at ? item.updated_at : item.created_at;
        item.trackBy = item.id + timestamp;
        return item;
      }
    }
  }
})();

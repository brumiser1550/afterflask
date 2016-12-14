/**
 * Created by Brandon on 10/3/2016.
 */

cleanApp.controller('technicianController', function ($scope, $http) {
    // $scope.user = 0;
    $scope.average_score = 0;
    $scope.average_score_percent = 0;
    $scope.total = 0;
    $scope.num_levels = 0;
    $scope.totals = {};
    $scope.feedback = [];
    $scope.levels = [];
    $scope.technician = {};

    $scope.api.levels = angular.copy($scope.api.default);
    $scope.api.feedback = angular.copy($scope.api.default);

    $scope.user = window.location.pathname.split('/')[2];
    getTechnician();
    getFeedback($scope.api.feedback);

    $scope.loadMoreFeedback = function () {
        $scope.api.feedback.data.offset = $scope.api.feedback.data.offset + $scope.api.feedback.data.limit;
        getFeedback($scope.api.feedback);
    };

    function getTechnician() {
        $http({
            method: 'GET',
            url: '/api/v1/technicians/' + $scope.user
        }).then(function (response) {
            $scope.technician = response.data;
            angular.forEach($scope.technician.feedback_totals, function (value, key) {
                if (value.value > 0) {
                    $scope.total += value.total;
                }
                if (value.value > $scope.num_levels) {
                    $scope.num_levels = value.value;
                }
            });
            angular.forEach($scope.technician.feedback_totals, function (value, key) {
                if (value.value > 0) {
                    // $scope.levels[value.value] = {};
                    $scope.average_score += value.value * value.total;
                    $scope.technician.feedback_totals[key].percent = value.total / $scope.total * 100;
                }
            });
            $scope.average_score_percent = $scope.average_score / $scope.total * 25;
            $scope.average_score = $scope.average_score / $scope.total;

        }, function (response, error_code) {
            console.log(response);
        });
    }

    function getFeedback(params) {
        $scope.api.feedback.busy = true;
        $http({
            method: 'GET',
            url: '/api/v1/feedback/' + $scope.user,
            params: params.data
        }).then(function (response) {
            // $scope.feedback = response.data.results;
            angular.forEach(response.data.results, function (value, key) {
                if (!$scope.containsObject(value, $scope.feedback)) {
                    $scope.feedback.push(value);
                }
            });
            $scope.api.feedback.busy = false;
            if (response.data.next == null) {
                $scope.api.feedback.done = true;
            }
            console.log($scope.feedback);
        }, function (response, error_code) {
            console.log(response);
        });
    }


});
/**
 * Created by Brandon on 10/3/2016.
 */
cleanApp.controller('companyController', function ($scope, $http, $timeout) {
    $scope.loading = false;
    $scope.total = 0;
    $scope.totals = {};
    $scope.feedback = {};
    $scope.jobs = [];
    $scope.levels = [];
    $scope.date.active_range = "this";

    $scope.api.levels = angular.copy($scope.api.default);
    $scope.api.jobs = angular.copy($scope.api.default);

    $scope.total_feedback = 0;
    $scope.total_response = 0;
    $scope.response_rate = 0;

    $scope.loadMoreJobs = function () {
        $scope.api.jobs.data.offset = $scope.api.jobs.data.offset + $scope.api.jobs.data.limit;
        getJobs($scope.api.jobs);
    };

    $scope.timeout = 0;
    var sync = function () {
        $timeout(function () {
            $scope.timeout = 1000000000;
            getJobs($scope.api.default);
            getLevels($scope.api.default);
            sync();
        }, $scope.timeout);
    };
    sync();

    $scope.fetchNewData = function () {
        $scope.jobs = [];
        getJobs($scope.api.default);
        getLevels($scope.api.default);
    };

    function getLevels(params) {
        $http({
            method: 'GET',
            url: '/api/v1/feedback-levels/',
            params: params.data
        }).then(function (response) {
            $scope.response_rate = 0;
            $scope.levels = response.data.results;
            angular.forEach(response.data.results, function (value, key) {
                $scope.total_feedback += value.count;
                if (value.value != 0) {
                    $scope.total_response += value.count;
                }
                $scope.levels[value.value] = value;
            });
            $scope.response_rate = $scope.total_response / $scope.total_feedback * 100;
        }, function (response, error_code) {
            console.log(response);
        });
    }

    function getJobs(params) {
        $scope.api.jobs.busy = true;
        $http({
            method: 'GET',
            url: '/api/v1/jobs/',
            params: params.data
        }).then(function (response) {
            angular.forEach(response.data.results, function (value, key) {
                if (!$scope.containsObject(value, $scope.jobs)) {
                    $scope.jobs.push(value);
                }
            });
            $scope.api.jobs.busy = false;
            if (response.data.next == null) {
                $scope.api.jobs.done = true;
            }
        }, function (response, error_code) {
            console.log(response);
        });
    }

});
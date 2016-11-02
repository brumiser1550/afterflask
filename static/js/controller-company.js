/**
 * Created by Brandon on 10/3/2016.
 */

cleanApp.controller('companyController', function ($scope, $http) {
    $scope.total = 0;
    $scope.totals = {};
    $scope.feedback = {};
    $scope.jobs = {};
    $scope.levels = [];
    get_levels();
    get_feedback();

    function get_levels() {
        $http({
            method: 'GET',
            url: '/api/v1/feedback-levels/'
        }).then(function (response) {
            angular.forEach(response.data, function (value, key) {
                value.count = 0;
                $scope.levels[value.value] = value;
            });
            get_overview();
        }, function (response, error_code) {
            console.log(response);
        });
    }

    function get_overview() {
        $http({
            method: 'GET',
            url: '/api/v1/jobs/'
        }).then(function (response) {
            $scope.jobs = response.data;
        }, function (response, error_code) {
            console.log(response);
        });
    }

    function get_feedback() {
        $http({
            method: 'GET',
            url: '/api/v1/feedback/'
        }).then(function (response) {
            console.log(response);
            $scope.feedback = response.data;
            feedback_totals();
        }, function (response, error_code) {
            console.log(response);
        });
    }

    function feedback_totals() {
        $scope.total = $scope.feedback.length;
        for (var i = 0; i < $scope.total; i++) {
            $scope.levels[$scope.feedback[i].level.value].count++;
        }
        console.log($scope.levels);
    }

});
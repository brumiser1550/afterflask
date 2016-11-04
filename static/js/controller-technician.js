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
    $scope.feedback = {};
    $scope.levels = [];
    $scope.technician = {};

    $scope.$watch("user", function(){
        get_technician();
        get_levels();
    });

    function get_technician() {
        console.log('/api/v1/technicians/' + $scope.user);
        $http({
            method: 'GET',
            url: '/api/v1/technicians/' + $scope.user
        }).then(function (response) {
            console.log(response);
            $scope.technician = response.data;
        }, function (response, error_code) {
            console.log(response);
        });
    }

    function get_levels() {
        $http({
            method: 'GET',
            url: '/api/v1/feedback-levels/'
        }).then(function (response) {
            angular.forEach(response.data, function (value, key) {
                value.count = 0;
                value.percent = 0;
                $scope.levels[value.value] = value;
                if (value.value > 0) {
                    $scope.num_levels++;
                }
            });
            get_feedback();
        }, function (response, error_code) {
            console.log(response);
        });
    }

    function get_feedback() {
        console.log("do feedback");
        $http({
            method: 'GET',
            url: '/api/v1/feedback/' + $scope.user
        }).then(function (response) {
            $scope.feedback = response.data;
            feedback_totals();
        }, function (response, error_code) {
            console.log(response);
        });
    }

    function feedback_totals() {
        console.log("do feedback totals");
        $scope.total = 0;

        angular.forEach($scope.feedback, function (value, key) {
            if (value.level.value > 0) {
                $scope.total++;
            }
            $scope.levels[value.level.value].count++;
        });
        angular.forEach($scope.feedback, function (value, key) {
            if (value.level.value > 0) {
                $scope.average_score += value.level.value;
                $scope.levels[value.level.value].percent = $scope.levels[value.level.value].count / $scope.total * 100;
            }
        });
        $scope.average_score_percent = $scope.average_score / $scope.total * 25;
        $scope.average_score = $scope.average_score / $scope.total;
    }

});
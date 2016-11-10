/**
 * Created by Brandon on 11/9/2016.
 */

cleanApp.controller('feedbackController', function ($scope, $http, $filter) {
    $scope.contact = {};
    $scope.jobs = {};
    $scope.feedback = {};
    $scope.jobs = {};
    $scope.levels = [];


    $scope.updateFormattedDate = function () {
        $scope.contact.completed__date = $filter('date')($scope.completed, "yyyy-MM-dd");
    };

    $scope.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
    };

    $scope.popup2 = {
        opened: false
    };
    $scope.open2 = function () {
        $scope.popup2.opened = true;
    };

    $scope.get_jobs = function () {
        console.log($scope.contact);
        $http({
            method: 'GET',
            url: '/api/v1/jobs/',
            params: $scope.contact
        }).then(function (response) {
            console.log(response);
            $scope.jobs = response.data;
        }, function (response, error_code) {
            console.log(response);
        });
    }

});
/**
 * Created by Brandon on 10/3/2016.
 */

cleanApp.controller('companyController', function ($scope, $http) {
    $scope.feedback = get_feedback();

    function get_feedback() {
        $http({
            method: 'GET',
            url: '/api/v1/feedback/'
        }).then(function (response) {
            $scope.feedback = response.data;
            console.log($scope.feedback);
        }, function (response, error_code) {
            console.log(response);
        });
    }

});
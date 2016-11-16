/**
 * Created by Brandon on 10/3/2016.
 */

cleanApp.service('CleanAPI', function ($http) {
    this.options = {
        url: "",
        offset: 0,
        limit: 25,
        busy: false,
        results: []
    };

    this.query = function(params)
    {
        params.busy = true;
        $http({
            method: params.method,
            url: params.url,
            params: params.data
        }).then(function (response) {
            console.log(response);
            angular.forEach(response.data.results, function (value, key) {
                if (!containsObject(value, params.results)) {
                    params.results.push(value);
                }
            });
            params.busy = false;
            if (response.data.next == null) {
                params.done = true;
            }
        }, function (response, error_code) {
            console.log(response);
        });
    };

    var containsObject = function(obj, list) {
        var i;
        for (i = 0; i < list.length; i++) {
            if (angular.equals(list[i], obj)) {
                return true;
            }
        }
        return false;
    };
    // this.getData = function () {
    //     if (this.busy) return;
    //     this.busy = true;
    //
    //     var url = "https://api.reddit.com/hot?after=" + this.after + "&jsonp=JSON_CALLBACK";
    //     $http.jsonp(url).success(function (data) {
    //         var items = data.data.children;
    //         for (var i = 0; i < items.length; i++) {
    //             this.items.push(items[i].data);
    //         }
    //         this.after = "t3_" + this.items[this.items.length - 1].id;
    //         this.busy = false;
    //     }.bind(this));
    // };

});

cleanApp.controller('companyController', function ($scope, $http, $timeout, CleanAPI) {
    $scope.loading = false;
    $scope.total = 0;
    $scope.totals = {};
    $scope.feedback = {};
    $scope.jobs = [];
    $scope.levels = [];

    $scope.api = {};
    $scope.api.default = {
        url: "",
        method: "GET",
        data: {
            offset: 0,
            limit: 25
        },
        busy: true,
        done: false,
        results: []
    };
    $scope.api.levels = angular.copy($scope.api.default);
    $scope.api.jobs = angular.copy($scope.api.default);
    // $scope.api.jobs.url = "/api/v1/feedback-levels/";
    // $scope.jobs2 = CleanAPI.query($scope.api.jobs);

    $scope.total_feedback = 0;
    $scope.total_response = 0;
    $scope.response_rate = 0;
    function getLevels() {
        $http({
            method: 'GET',
            url: '/api/v1/feedback-levels/',
            params: $scope.api.levels
        }).then(function (response) {
            next = response.data.next;
            $scope.levels = response.data.results;
            angular.forEach(response.data.results, function (value, key) {
                $scope.total_feedback += value.count;
                if(value.value!=0){
                    $scope.total_response += value.count;
                }
                $scope.levels[value.value] = value;
            });
            console.log($scope.total_response);
            console.log($scope.total_feedback);
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
            // $scope.jobs = response.data.results;
            console.log(response);
            angular.forEach(response.data.results, function (value, key) {
                if (!$scope.containsObject(value, $scope.jobs)) {
                    $scope.jobs.push(value);
                }
            });
            $scope.api.jobs.busy = false;
            if(response.data.next == null) {
                $scope.api.jobs.done = true;
            }
        }, function (response, error_code) {
            console.log(response);
        });
    }

    $scope.loadMoreJobs = function () {
        $scope.api.jobs.data.offset = $scope.api.jobs.data.offset + $scope.api.jobs.data.limit;
        getJobs($scope.api.jobs);
    };

    $scope.timeout = 0;
    var sync = function () {
        $timeout(function () {
            $scope.timeout = 1000000000;
            getJobs($scope.api.default);
            getLevels();
            sync();
        }, $scope.timeout);
    };
    sync();

    $scope.containsObject = function (obj, list) {
        var i;
        for (i = 0; i < list.length; i++) {
            if (angular.equals(list[i], obj)) {
                return true;
            }
        }
        return false;
    };

});
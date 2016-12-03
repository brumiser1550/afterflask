/**
 * Created by Brandon on 10/3/2016.
 */

cleanApp.controller('reviewsController', function ($scope, $http, $location, $anchorScroll, $filter) {
    $scope.isNavCollapsed = true;
    $scope.alerts = messages;
    $scope.closeAlert = function (index) {
        $scope.alerts.splice(index, 1);
    };
    $scope.loaded = true;

    $scope.updateFormattedDate = function (d) {
        return $filter('date')(d, "yyyy-MM-dd");
    };

    $scope.query_string = "";
    $scope.getQueryString = function () {
        var qs = $location.search();
        if (qs) {
            $scope.query_string += "#?";
            angular.forEach(qs, function (value, key) {
                $scope.query_string += key + "=" + value + "&";
            });
            $scope.query_string.slice(0, -1);
        }
    };

    $scope.getQueryString();
    $scope.$on('$routeUpdate', function () {
        console.log("route update");
        $scope.getQueryString();
    });

    $scope.date = {
        active_range: "",
        date_to: "",
        date_from: ""
    };

    var searchObject = $location.search();
    var offset = new Date().getTimezoneOffset() * 60000;
    if (searchObject.date_to) {
        $scope.date.active_range = "custom";
        $scope.date.date_to = new Date(searchObject.date_to);
        $scope.date.date_to.setTime($scope.date.date_to.getTime() + offset);
    } else {
        $scope.date.date_to = new Date();
    }
    if (searchObject.date_from) {
        $scope.date.active_range = "custom";
        $scope.date.date_from = new Date(searchObject.date_from);
        $scope.date.date_from.setTime($scope.date.date_from.getTime() + offset);
    } else {
        $scope.date.date_from = new Date();
        $scope.date.date_from = $scope.getMonday($scope.date.date_to);
    }
    $scope.api = {};
    $scope.api.default = {
        url: "",
        method: "GET",
        data: {
            offset: 0,
            limit: 25,
            date_from: $scope.updateFormattedDate($scope.date.date_from),
            date_to: $scope.updateFormattedDate($scope.date.date_to)
        },
        busy: true,
        done: false,
        results: []
    };

    $scope.updateDateRange = function () {
        if ($scope.date.active_range == "this") {
            $scope.date.date_to = new Date();
            $scope.date.date_from = $scope.getMonday($scope.date.date_to);
        }
        if ($scope.date.active_range == "last") {
            $scope.date.date_to = new Date();
            $scope.date.date_to.setDate($scope.date.date_to.getDate() - 7);
            $scope.date.date_from = $scope.getMonday($scope.date.date_to);
            $scope.date.date_to = $scope.getFriday($scope.date.date_to);
        }
        $scope.api.default.data.date_from = $scope.updateFormattedDate($scope.date.date_from);
        $scope.api.default.data.date_to = $scope.updateFormattedDate($scope.date.date_to);
        $location.search('date_from', $scope.api.default.data.date_from);
        $location.search('date_to', $scope.api.default.data.date_to);
    };

    $scope.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
    };

    $scope.date.date_from_pop = {
        opened: false
    };
    $scope.openDateFromPop = function () {
        $scope.date.date_from_pop.opened = true;
    };

    $scope.date.date_to_pop = {
        opened: false
    };
    $scope.openDateToPop = function () {
        $scope.date.date_to_pop.opened = true;
    };

    $scope.getMonday = function (d) {
        d = new Date(d);
        var day = d.getDay();
        var diff = d.getDate() - day + (day == 0 ? -6 : 1); // adjust when day is sunday
        return new Date(d.setDate(diff));
    };

    $scope.getFriday = function (d) {
        d = new Date(d);
        var day = d.getDay();
        var diff = d.getDate() - day + 5;
        return new Date(d.setDate(diff));
    };

    $scope.containsObject = function (obj, list) {
        var i;
        for (i = 0; i < list.length; i++) {
            if (angular.equals(list[i], obj)) {
                return true;
            }
        }
        return false;
    };

    $scope.getParameterByName = function (name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(location.search);
        return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    };


    $scope.months = [{
        value: "01",
        label: "Jan(01)"
    }, {
        value: "02",
        label: "Feb(02)"
    }, {
        value: "03",
        label: "Mar(03)"
    }, {
        value: "04",
        label: "Apr(04)"
    }, {
        value: "05",
        label: "May(05)"
    }, {
        value: "06",
        label: "Jun(06)"
    }, {
        value: "07",
        label: "Jul(07)"
    }, {
        value: "08",
        label: "Aug(08)"
    }, {
        value: "09",
        label: "Sep(09)"
    }, {
        value: "10",
        label: "Oct(10)"
    }, {
        value: "11",
        label: "Nov(11)"
    }, {
        value: "12",
        label: "Dec(12)"
    }];
    $scope.years = [];
    var now = new Date();
    var this_year = now.getFullYear();
    for (var i = 0; i < 10; i++) {
        $scope.years.push({
            value: this_year + i,
            label: this_year + i
        });
    }

    $scope.applyPromo = function () {
        $scope.errors.promo = '';
        $scope.hasError = $scope.checkForError();
        var data = {
            action: 'apply_promo',
            cart: $scope.cart
        };
        $http({
            method: 'POST',
            url: 'http/',
            data: data
        }).then(function (data) {
            if (data.data.success) {
                $scope.cart.discount = data.data.data;
                $scope.cart.promo = '';
            }
        }, function (data, error_code) {
            $scope.errors.promo = data.data.message;
            $scope.hasError = $scope.checkForError();
            document.getElementById('error-placeholder').scrollIntoView();
        });
    };
});

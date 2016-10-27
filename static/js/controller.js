/**
 * Created by Brandon on 10/3/2016.
 */
(function() {
    'use strict';
    var reviewsApp = angular.module('reviewsApp', ['ui.bootstrap']);
    reviewsApp.controller('reviewsController', function($scope, $http, $location, $anchorScroll) {
        $scope.isNavCollapsed = true;
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

        $scope.applyPromo = function() {
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
            }).then(function(data) {
                if (data.data.success) {
                    $scope.cart.discount = data.data.data;
                    $scope.cart.promo = '';
                }
            }, function(data, error_code) {
                $scope.errors.promo = data.data.message;
                $scope.hasError = $scope.checkForError();
                document.getElementById('error-placeholder').scrollIntoView();
            });
        };

        $scope.alerts = messages;

        $scope.addAlert = function() {
            $scope.alerts.push({
                msg: 'Another alert!'
            });
        };

        $scope.closeAlert = function(index) {
            $scope.alerts.splice(index, 1);
        };

        $scope.loaded = true;

    });

}());
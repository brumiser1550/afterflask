/**
 * Created by Brandon on 10/3/2016.
 */
var cleanApp = angular.module('cleanApp', ['ngAnimate', 'ui.bootstrap']);
// var base = angular.module('base', ['http', 'location', 'anchorScroll']);
// var companies = angular.module('companies', []);

cleanApp.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});
cleanApp.filter('filterHtmlChars', function () {
    return function (html) {
        var filtered = angular.element('<div>').html(html).text();
        return filtered;
    }
});
cleanApp.run(['$location', function ($location) {
    //Allows us to navigate to the correct element on initialization
    if ($location.path() !== '' && $location.path() !== '/') {
        smoothScroll(document.getElementById($location.path().substring(1)), 500, function (el) {
            location.replace('#' + el.id);
        });
    }
}]);
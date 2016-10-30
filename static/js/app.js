/**
 * Created by Brandon on 10/3/2016.
 */
var cleanApp = angular.module('cleanApp', ['ui.bootstrap']);
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

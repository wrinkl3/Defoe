'use strict';

/**
 * @ngdoc directive
 * @name angularLoadingdots.directive:loadingDots
 * @description An AngularJS directive to display loading dots in the form of text"
 * # loadingDots
 */
angular.module('angularLoadingDots', [])
  .directive('loadingDots', ["$interval", function ($interval) {

    /**
     * Repeats a character n times
     * @param  {String} theChar The character to repeat
     * @param  {Number} count   The amount of times to repeat it
     * @return {String}         The string containing the character n times
     * @private
     */
    function repeatChar(theChar, count) {
      var str = '';
      while(count--) {
        str += theChar;
      }
      return str;
    }

    /**
     * Used to validate a number input coming from an html attribute as a string
     * And default to a value in case it wasn't provided.
     * It can optionally validate that the value is within a minimum and maximum range.
     * @param  {Number} value       The value
     * @param  {Number} defaultTo   The value to default to if value wasn't passed
     * @param  {Number} optMinValue Optional minimum value
     * @param  {Number} optMaxValue Optional maximum value
     * @return {Number}             The value passed in value if it was passed and between the optional min or max values.
     *                               Otherwise, returns the value to default to
     * @private
     */
    function numberValueOrDefault(value, defaultTo, optMinValue, optMaxValue) {
      //don't use if(!value) notation since 0  might be the desired value
      if(value === undefined || value === null) {
        return defaultTo;
      }

      //parse it since it comes
      value = parseInt(value, 10);

      if(optMinValue !== undefined && value < optMinValue) {
        value = optMinValue;
      }
      if(optMaxValue !== undefined && value > optMaxValue) {
        value = optMaxValue;
      }

      return value;
    }

    function link(scope, element, attributes) {
      //numeric values
      var min         = numberValueOrDefault(attributes.minDots, 0, 0);
      var max         = numberValueOrDefault(attributes.maxDots, 5, min + 1);
      var starting    = numberValueOrDefault(attributes.starting, min, min, max);
      var increment   = numberValueOrDefault(attributes.increment, 1);
      var interval    = numberValueOrDefault(attributes.interval, 300);

      var character   = attributes.character  || '.';
      var isLoading   = attributes.isLoading  || false;

      var intervalPromise  = null;
      var text = repeatChar(character, starting);

      //starts the interval
      function startInterval() {
        //cancel any previous interval so we don't have unreferenced intervals running
        if(intervalPromise) {
          $interval.cancel(intervalPromise);
        }
        var initialText = repeatChar(character, starting);
        element.text(initialText);
        intervalPromise = $interval(tick, interval);
        isLoading = true;
      }

      //stops the interval and empties the text
      function stopInterval() {
        if(intervalPromise) {
          $interval.cancel(intervalPromise);
          element.text('');
        }
        isLoading = false;
      }

      //callback for interval
      function tick() {
        //in theory shouldn't happen
        if(!isLoading) {
          return;
        }

        var length = text.length;
        if(length < max) {
          text = repeatChar(character, length + increment);
        } else {
          text = repeatChar(character, min);
        }
        element.text(text);
      }

      //listen for the "is-loading" attribute changes to start or stop
      scope.$watch(attributes.isLoading, function(loading) {
        if(loading) {
          startInterval();
        } else {
          stopInterval();
        }

      });

      element.on('$destroy', stopInterval);
    }

    return {
      restrict: 'AE',
      link: link
    };
  }]);

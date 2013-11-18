jQuery(document).ready(function ($) {
	'use strict';
	var $ctsearch = $('#buscador'),
		$ctsearchinput = $ctsearch.find('input.buscador-input'),
		$body = $('html,body'),
		openSearch = function () {
			$ctsearch.data('open', true).addClass('buscador-open');
			$ctsearchinput.focus();
			return false;
		},
		closeSearch = function () {
			$ctsearch.data('open', false).removeClass('buscador-open');
		};

	$ctsearchinput.on('click', function (e) {
		e.stopPropagation();
		$ctsearch.data('open', true);
	});

	$ctsearch.on('click', function (e) {
		e.stopPropagation();
		if (!$ctsearch.data('open')) {

			openSearch();

			$body.off('click').on('click', function (e) {
				closeSearch();
			});

		} else {
			if ($ctsearchinput.val() === '') {
				closeSearch();
				return false;
			}
		}
	});

});

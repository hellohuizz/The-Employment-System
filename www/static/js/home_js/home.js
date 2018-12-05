$(function() {
	var swiper = new Swiper('.swiper-container', {
		pagination: '.swiper-pagination',
		loop: true,
		paginationClickable: true,
		nextButton: '.swiper-button-next',
		prevButton: '.swiper-button-prev',
		spaceBetween: 30,
		effect: 'fade',
		autoplay:2000
	});
})
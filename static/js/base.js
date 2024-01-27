// Скролл страницы меняет цвет навигации
$(document).scroll(function(e) {
    $(window).scrollTop() > 30 ? $('.nav').addClass('nav-color') : $('.nav').removeClass('nav-color');
});
document.addEventListener("mousedown", function(event) {
    if (event.target.closest("::-webkit-scrollbar")) {
        event.preventDefault();
    }
});
// Модальное окно
$('#btn').click(function(){
	$.fancybox.open({
		src: '#hidden',
		type: 'inline',
		hideOnOverlayClick: true,
		touch: false
	});
});
// Гамабургер меню
$(document).ready(function() {
    $('.menu-burger__header').click(function() {
        $('.menu-burger__header, .header__nav').toggleClass('open-menu');
//        $('body').toggleClass('fixed-page');
    });
});
// Открытие списка меню тем
$('.menu').on('click', '.menu__item.dropdown-topics', function(){
    $('.dropdown-topics-content').toggleClass('opened-topics');
});
$(document).on('click', function(event) {
    if (!$(event.target).closest('.dropdown-topics').length) {
        $('.dropdown-topics-content').removeClass('opened-topics');
    }
});
// Проверка на галочку при регистрации
 $("#privacy").change(function(){
        if($(this).is(':checked')){
            $('.privacy-error').remove();
        }
    });
$('.modal-window').on('click', '.social-icon a', function(event){
    if (!privacy.checked){
        event.preventDefault();
        if (!$('.privacy-error').length){
            $('.modal-window').append('<div class="privacy-error">Пожалуйста, согласитесь с правилами пользования</div>');
        }
    };
});
function checkCookies(){
    let cookieDate = localStorage.getItem('cookieDate');
    let cookieNotification = document.getElementById('cookie_notification');
    let cookieBtn = cookieNotification.querySelector('.cookie_accept');

    // Если записи про кукисы нет или она просрочена на 1 год, то показываем информацию про кукисы
    if( !cookieDate || (+cookieDate + 31536000000) < Date.now() ){
        cookieNotification.classList.add('show');
    }

    // При клике на кнопку, в локальное хранилище записывается текущая дата в системе UNIX
    cookieBtn.addEventListener('click', function(){
        localStorage.setItem( 'cookieDate', Date.now() );
        cookieNotification.classList.remove('show');
    })
}
checkCookies();
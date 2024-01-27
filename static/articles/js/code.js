// Автоматическая высота у textarea
$(document).on("input", "textarea", function () {
    $(this).outerHeight(133).outerHeight(this.scrollHeight);
});
/* Когда пользователь нажимает на кнопку,
переключение между скрытием и отображением раскрывающегося содержимого */
function drop_btn() {
    document.getElementById("myDropdown").classList.toggle("show");
    document.getElementById("arrow").classList.toggle("open");
  }

// Закрывает выпадающее меню, если пользователь щелкает за его пределами
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }
// Кнопка лайка
$(function() {
    $( ".button-like" ).click(function() {
      $(this).find('i').toggleClass( "press", 1000 );
    });
  });
$(function() {
    $( ".button-replies" ).click(function() {
      $(this).find('#arrow').toggleClass("open");
      if ($(this).next(".show-replies").attr('hidden')){
        $(this).next(".show-replies").attr('hidden',false)
      }
      else{
        $(this).next(".show-replies").attr('hidden',true)
      }
//      $(this).next(".show-replies").css('display','block');
    });
  });
// Кнопка для выхода с формы отправки комментария
$('.comments').on("click", ".btn-form-quit ", function () {
    $(this).parent().parent().css('display','none');
});
// Открытие формы для отправки ответа на комментарий
$('.comments').on("click", ".comment-answer", function () {
    $(this).parent().parent().find('.form-reply').first().css('display','block');
});
// Открытие формы для редактирования комментария
$('.comments').on("click", ".edit-comment", function () {
    comment_id = $(this).parent().parent().attr('comment-id');
    $(this).parent().parent().find(`.form-edit[value='${comment_id}']`).css('display','block');
});
// Модальное окно для подтверждения на удаление комментария
$('.comments').on('click','.delete-comment',function(){
	$.fancybox.open({
		src: '#hidden-comment-delete',
		type: 'inline',
		touch: false,
        afterClose: function() {
            $('#button-delete-comment').off('click');
        }
	});
});

// Добавление всем ссылка в тексте атрибут rel="nofollow"
$('.main-text a').attr('rel', 'nofollow');
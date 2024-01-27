// csrftoken
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// Удаление комментария ajax
$('.comments').on('click','.delete-comment',function(){
    $('#button-delete-comment').on('click',()=>{
        var comment_id = $(this).attr('value');
        event.preventDefault();
        $.ajax({
          url: "http://127.0.0.1:8000/delete_comment/",
          type: "POST",
          dataType: "json",
          data: {
            'comment_id': comment_id,
          },
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie('csrftoken'),
          },
          success: data => {
            $('.comments').find(`.comment[comment-id='${comment_id}']`).remove();
          },
          error: function(error){
            console.log(error);
          }
        });
    });
});
// Редактирование комментария
$('.comments').on('submit','.form-edit',function(){
    var text = $(this).find('textarea').val();
    event.preventDefault();
    if (text.trim() !== ''){
        var comment_id = $(this).attr('value');
        $.ajax({
          url: "http://127.0.0.1:8000/edit_comment/",
          type: "POST",
          dataType: "json",
          data: {
            'comment_id': comment_id,
            'new_text': text,
          },
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie('csrftoken'),
          },
          success: data => {
            $(this).css('display','none');
            $(this).parent().find('.comment-text').first().text(data['new_text']);
          },
          error: function(error){
            console.log(error);
          }
        });
    }
});
// Лайк на пост
$('.form-like').submit(function(){
    var is_fan_article = ($('.form-like').attr('is-liked') === 'True');
    event.preventDefault();
    if (is_fan_article){
        var url = "/likes/remove_like_article/";
      }
    else{
        var url = "/likes/add_like_article/";
    }
    var article_id = $(this).attr('value');
    var is_authenticated = ($(this).attr('auth') === 'True');
    $.ajax({
      url: url,
      type: "POST",
      dataType: "json",
      data: {
        'article_id':article_id,
      },
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie('csrftoken'),
      },
      success: function(data){
        $('.like-article').removeClass('show-like').addClass('hide');
            setTimeout(function(){
               $('#like').text(data['total_likes']);
               $('.like-article').removeClass('hide').addClass('show-like');
            }, 200);
        if (data['is_liked']){
            $('.form-like').attr('action','/likes/remove_like_article/');
            $('.form-like').attr('is-liked','True');
        }
        else{
            $('.form-like').attr('action','/likes/add_like_article/');
            $('.form-like').attr('is-liked','False');
        }
      },
      error: function(error){
         if (!is_authenticated){
             $.fancybox.open({
                src: '#hidden',
                type: 'inline',
                hideOnOverlayClick: true,
                touch: false
            });
         }
         else {
            console.log(error);
         }
      }
    });
});
// Лайк комментария
$('.comments').on('submit','.form-like-comment',function(){
    var is_fan_comment = ($(this).attr('is-liked') === 'True');
    event.preventDefault();
    if (is_fan_comment){
        var url = "/likes/remove_like_comment/";
      }
    else{
        var url = "/likes/add_like_comment/";
    }
    var is_authenticated = ($('.form-like').attr('auth') === 'True');
    $.ajax({
      url: url,
      type: "POST",
      dataType: "json",
      data: {
        'comment_id': $(this).attr('value'),
      },
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie('csrftoken'),
      },
      success: data => {
        $(this).find('.comment-number-like').removeClass('show-like').addClass('hide');
            setTimeout(()=>{
               $(this).find('.comment-number-like').text(data['total_likes']);
               $(this).find('.comment-number-like').removeClass('hide').addClass('show-like');
            }, 200);
        if (data['is_liked']){
            $(this).attr('action','/likes/remove_like_comment/');
            $(this).attr('is-liked','True');
            $(this).find('i').addClass('press');
        }
        else{
            $(this).attr('action','/likes/add_like_comment/');
            $(this).attr('is-liked','False');
            $(this).find('i').removeClass('press');
        }
      },
      error: function(error){
        if (!is_authenticated){
             $.fancybox.open({
                src: '#hidden',
                type: 'inline',
                hideOnOverlayClick: true,
                touch: false
            });
         }
         else {
            console.log(error);
         }
      }
    });
});
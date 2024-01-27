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
// Сохранение профиля пользователя
$('#form').submit(function(){
    event.preventDefault()
    var user_name = $("#user-name").val();
    var description = $("#description").val();
    var user_social = $("#user-social").val();
    var user_id = $(this).attr('value');
    $.ajax({
      url: `save_user_settings/${user_id}`,
      type: "POST",
      dataType: "text",
      data: {
        'user_name': user_name,
        'description': description,
        'user_social': user_social,
      },
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie('csrftoken'),
      },
      success: function(data){
        $(".profile-name").text(user_name)
        $(".profile-alert").css({'opacity':1,'visibility':'visible'});
        setTimeout(() => {$(".profile-alert").css({'opacity':0,'visibility': 'hidden'});}, 2000);
      },
      error: function(error){
        console.log('error');
      }
    });
});
$(document).ready(function(){
    $('.saved-film').click(function(e){
        e.preventDefault();
        var post_id = $(this).data('post-id');
        var csrf_token = "{{ csrf_token }}";
        var url = "saved/";
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'post_id': post_id,
                'csrfmiddlewaretoken': csrf_token,
                'action': 'saved'
            },
            success: function(response){
                // Qo'shilgan likelar sonini yangilash
                $('.kn-saved').text(response.saqlash + '');
            },
            error: function(response){
                console.log('Saqlanmadi');
            }
        });
    });
});
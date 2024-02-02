$(document).ready(function(){
    $('.like-btn').click(function(e){
        e.preventDefault();
        var post_id = $(this).data('post-id');
        var csrf_token = "{{ csrf_token }}";
        var url = "like/";
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'post_id': post_id,
                'csrfmiddlewaretoken': csrf_token,
                'action': 'like'
            },
            success: function(response){
                // Qo'shilgan likelar sonini yangilash
                $('.like-count').text(response.likes_count);
                $('.kn-rat').text(response.kn_rat + '%');
            },
            error: function(response){
                console.log('');
            }
        });
    });
});

    //DIslike uchun kodlar
    $(document).ready(function(){
    $('.dislike-btn').click(function(e){
        e.preventDefault();
        var post_id = $(this).data('post-id');
        var csrf_token = "{{ csrf_token }}";
        var url = "dislike/";
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'post_id': post_id,
                'csrfmiddlewaretoken': csrf_token,
                'action': 'dislike'
            },
            success: function(response){
                // Qo'shilgan likelar sonini yangilash
                $('.like-count').text(response.likes_count);
                $('.kn-rat').text(response.kn_rat + '%');
            },
            error: function(response){
                console.log('');
            }
        });
    });
});
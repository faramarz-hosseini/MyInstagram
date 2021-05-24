let offset = 0;
        $(document).ready(function () {
            $.ajax({
                    type: "GET",
                    url: `http://localhost:8000/activity-feed-json/${offset}`,
                    beforeSend: function () {
                        $("#posts").append(`<img class='spinner1' width="50" height="50" src={% static 'instagram/ClassicImpureKagu-size_restricted.gif' %}>`)
                    },
                    complete: function () {
                        $(".spinner1").hide()
                    },
                    success: function (posts) {
                        for (let post in posts){
                            $("#posts").append(`<div class="border mt-5 container-fluid rounded-3 p-5">
                                    <pre><img width="80" height="80" class="clearfix img-fluid rounded-circle mt-4" src=${posts[post]["profile_pic"]}>  ${posts[post]['publisher']}

Posted: ${posts[post]['date_posted']}
                                    </pre>
                                    <img class="mb-1" width="90%" src=${posts[post]['post']}>
                                    <p class="mt-4">${posts[post]['likes']} likes</p>
                                    <p class="mt-14"><strong>${posts[post]['publisher']}:</strong>  ${posts[post]['caption']}</p>
                                </div>`
                            )
                        }
                        offset += 5
                    }
                })
        })
        $(window).scroll(function() {
            if ($(window).scrollTop() + $(window).height() == $(document).height()){
                $.ajax({
                    type: "GET",
                    url: `http://localhost:8000/activity-feed-json/${offset}`,
                    beforeSend: function () {
                        $("#posts").append(`<img class='spinner1' width="50" height="50" src={% static 'instagram/ClassicImpureKagu-size_restricted.gif' %}>`)
                    },
                    complete: function () {
                        $(".spinner1").hide()
                    },
                    success: function (posts) {
                        for (let post in posts){
                            $("#posts").append(`<div class="border mt-5 container-fluid rounded-3 p-5">
                                    <pre><img width="80" height="80" class="clearfix img-fluid rounded-circle mt-4" src=${posts[post]["profile_pic"]}>  ${posts[post]['publisher']}

Posted: ${posts[post]['date_posted']}
                                    </pre>
                                    <img class="mb-1" width="90%" src=${posts[post]['post']}>
                                    <p class="mt-4">${posts[post]['likes']} likes</p>
                                    <p class="mt-4"><strong>${posts[post]['publisher']}:</strong>  ${posts[post]['caption']}</p>
                                </div>`
                            )
                        }
                        initialize = false
                        offset += 5
                    }
                })
            }
        });
$(document).ready(function () {
    $('.exit-btn').on('click', function (e) {
        e.preventDefault()
        id = $(e.target).attr('data-id')
        console.log(id)
        $.post('sumbitExit/', {id}, function (response, status) {
            $('button').attr('disabled' , true)
            if (status == 'success') {
                alert("با موفقیت ثبت شد")
                location.reload()
            }
            $('button').attr('disabled' , false)
        })
    });
    $('.enter-btn').on('click', function (e) {
        e.preventDefault()
        id = $(e.target).attr('data-id')
        console.log(id)
        $.post('sumbitEnter/', {id}, function (response, status) {
            if (status == 'success') {
                alert("با موفقیت ثبت شد")
                location.reload()

            }
        })
    });

})
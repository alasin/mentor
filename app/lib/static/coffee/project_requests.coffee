$ ->
    $(".accept, .reject").on "click", (e) ->
        $(@).parent().parent().fadeOut()
        if "accept" in e.currentTarget.classList
            state = "accept"
        else
            state = "reject"
        $.post window.href, 
            request_id: e.currentTarget.name
            state: state
            (response) ->
                console.log response

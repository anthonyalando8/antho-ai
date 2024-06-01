$(document).ready(function(){
    function get_navbar_height(){
        return $(".navbar").outerHeight(true)
    }
    function set_container_height(new_height){
        $("#body-container").css({
            "height": `calc(100% - ${new_height}px)`,
            "max-height": `calc(100% - ${new_height}px)`,
            "top": `${new_height}px`
        })
    }
    $(window).resize(function(){
        set_container_height(get_navbar_height())
    })
    set_container_height(get_navbar_height())
    const elementToObserve = document.querySelector('.navbar');

    // Create a new instance of ResizeObserver
    const resizeObserver = new ResizeObserver(entries => {
        for (let entry of entries) {
            //console.log('Element resized:', entry.contentRect.width, entry.contentRect.height);
            set_container_height(entry.contentRect.height)
        }
    });

    // Start observing the element
    resizeObserver.observe(elementToObserve);

    function retrieve_notification(){
        const formData = new FormData();
        var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        formData.append("gmc", "true");
        formData.append("csrfmiddlewaretoken", csrf_token)

        fetch("/", {
            method: "POST",
            body: formData,
        })
        .then(response => {
            return response.json()
        }).then(data =>{
            if (Object.keys(data).length === 0 && data.constructor === Object) {
                console.log("Data is empty");
            }
            let response_code = data.status_response.status_code
            let response_message = data.status_response.status_text
            if(response_code == "ok"){
                let unread_responses = data.unread_response_count;
                let messages = data.messages;
                if(unread_responses > 0){
                    $("#fa-bell-notification").addClass("fa-shake");
                    $("#btn-bell-notification").addClass("text-danger")
                    $("#notification-badge").removeClass("d-none")
                    $("#btn-bell-notification").addClass("text-warning")
                    $("#notification-badge").text(unread_responses > 99 ? "99+": unread_responses)
                }else{
                    $("#notification-badge").addClass("d-none")
                    $("#btn-bell-notification").addClass("text-light")
                }
                if (messages.length > 0){
                    console.log("user has messages")
                }else{
                    console.log("user has no messages")
                }
                
            }else{
                console.log("Error received")
                $("#btn-bell-notification").addClass("text-light")
            }
            console.log()
            
        })
        .catch(error => {
            console.error("Error submitting form:", error);
        });

    }
    retrieve_notification()


})

//$(document).ready(function(){
    function createToast(message, status){
        var toast = document.createElement('div');
        toast.classList.add('position-fixed');
        //toast.classList.add('top-0');
        toast.style.top = "56px"
        toast.classList.add('end-0','p-3')
        toast.style.zIndex = "10000";
        toast.style.maxWidth = "100vw"
        var bg_color = "bg-success"
        if (status == 300){
            bg_color = "bg-info"
        }else if(status != 200){
            bg_color = "bg-danger"
        }
        var toast_html = `
        <div id="liveToast" class="toast hide ${bg_color}" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
            <strong class="me-auto">SoftConnect</strong>
            <small>Now</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body text-light">
            ${message}
        </div>
        </div>
        `
        toast.innerHTML = toast_html
        document.getElementById("body").appendChild(toast)
        $("#liveToast").show()
        setTimeout(function(){
            toast.remove()
        },5500)

    }
//});
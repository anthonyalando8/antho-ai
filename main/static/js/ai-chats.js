
$(document).ready(function(){
    var converter = new showdown.Converter();

    var user_avatar = "https://ik.imagekit.io/anthonyalando/Soft_Connect/user.png?updatedAt=1682239876486"
    var softchat_avatar = "https://ik.imagekit.io/anthonyalando/Soft_Connect/cpu.png?updatedAt=1715174298728"
    var converted_to_html_user_avatar_name = converter.makeHtml(`<div markdown="1" class="d-flex m-2 align-items-center flex-row my-2"><div markdown="1">![your image](${user_avatar} =32x32 "You")</div><div markdown="1" class="mx-md-3 mx-2">**You**</div></div>`)
    var converted_to_html_softchat_avatar_name = converter.makeHtml(`<div markdown="1" class="d-flex m-2 align-items-center flex-row my-2"><div markdown="1">![soft connect logo](${softchat_avatar} =32x32 "SoftChatAI")</div><div markdown="1" class="mx-md-3 mx-2"> **SoftChatAI**</div></div>`)
               
    $("#ai_chat_form").submit(function(event){
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            success: function(response){
                // Check if response is empty
                if ($.isEmptyObject(response)) {
                    console.log("Response is empty");
                    return;
                } 
                try {
                    // Attempt to parse JSON
                    var jsonData = JSON.parse(response);
                    
                    var htmlData = ""
                    var chathistory = "new_chat"
                    jsonData.forEach(element => {
                        var message = element.fields.message;
                        var response = element.fields.response;
                        var image = element.fields.image;
                        // Create a Showdown converter
                        var image_html = ""
                        
                        if(image != null && image != ""){
                            image_html = converter.makeHtml(`<div markdown="1" style="max-width: 500px; max-height: 500px" class="m-2 overflow-hidden">![Message Image](${image})</div>`)
                        }
                        // Convert Markdown to HTML
                        var response_to_html = converter.makeHtml(response)
                        var response_ai_name = converted_to_html_softchat_avatar_name+`<div class="ml-2 m-2" >${response_to_html}</div>`;
                        var message_user_name = converted_to_html_user_avatar_name + `<div class="ml-2 m-2">${image_html}${message}</div>`;
                        htmlData += (message_user_name+response_ai_name)
                        chathistory = element.fields.chatHistory
                    });
                    $("#chat").html(htmlData)
                    $("#get_ai_chats").attr("value", chathistory)
                    console.log($("#get_ai_chats").attr("value"))

                } catch (error) {
                    console.error("Error parsing JSON:", error);
                }
               
            },
            error: function(error){
                console.log(error)
            }
        });

    });
    $("#btn_get_chats").click();


    
});

//$(document).ready(function(){
    var converter = new showdown.Converter();

    var user_avatar = "https://ik.imagekit.io/anthonyalando/Soft_Connect/user.png?updatedAt=1682239876486"
    var softchat_avatar = "https://ik.imagekit.io/anthonyalando/Soft_Connect/cpu.png?updatedAt=1715174298728"
    var converted_to_html_user_avatar_name = converter.makeHtml(`<div markdown="1" class="d-flex align-items-center flex-row mx-2 my-2"><div markdown="1">![your image](${user_avatar} =32x32 "You")</div><div markdown="1" class="mx-md-3 mx-2">**You**</div></div>`)
    var converted_to_html_softchat_avatar_name = converter.makeHtml(`<div markdown="1" class="d-flex align-items-center flex-row mx-2 my-2"><div markdown="1">![soft connect logo](${softchat_avatar} =32x32 "SoftChatAI")</div><div markdown="1" class="mx-md-3 mx-2"> **SoftChatAI**</div></div>`)
       
const form = document.getElementById('form');

// Add an event listener to the form submission
form.addEventListener('submit', async function(event) {
    // Prevent the default form submission
    event.preventDefault();
    var submitButton = $('#form button[type="submit"]');

    submitButton.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
    submitButton.attr("disabled","disabled");
    // Create a FormData object and populate it with form data
    const formData = new FormData(form);
    $('#form')[0].reset();
    // Send a POST request using the Fetch API
fetch(form.getAttribute("action"), {
    method: 'POST',
    body: formData
})
.then(response => {
    // Check if the response is a streaming response
    if (response.body && response.body.pipeTo) {
        // Create a new ReadableStream to read the response data
        const stream = new ReadableStream({
            start(controller) {
                const reader = response.body.getReader();
                
                // Read chunks of data as they arrive
                function read() {
                    reader.read().then(({ done, value }) => {
                        if (done) {
                            submitButton.html('<i class="fa-solid fa-paper-plane"></i>');
                            submitButton.removeAttr("disabled")
                            $('#id_message').attr('placeholder','Enter message');
                            $('#id_message').focus();
                            controller.close();
                            return;
                        }
                        // Process the received data (e.g., append to a DOM element)
                        // Convert Uint8Array to string
                        const text = new TextDecoder().decode(value);  
                        try {
                            // Parse the string as JSON
                            const jsonData = JSON.parse(text);
                            if("is_first" in jsonData && jsonData.is_first){
                                $("#chat").append(converted_to_html_user_avatar_name+`<div class="m-2">${jsonData.prompt}</div>`)
                                $("#chat").append(converted_to_html_softchat_avatar_name)
                                var response_html = converter.makeHtml(jsonData.res)
                                $("#chat").append(`<div id="response_${jsonData.message_id}" class="m-2">${response_html}</div>`)
                            }
                            if("is_error" in jsonData && jsonData.is_error){
                                $("#chat").append(
                                    `
                                    <div class="border m-2 rounded m-2 p-1 alert alert-danger d-flex align-items-center" role="alert">
                                        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>
                                        <div>
                                            Error occurred! Refresh this chat <a href="{% url 'chatbot:chat' %}" class="alert-link">Reload</a>
                                        </div>
                                        
                                    </div>
                                    <script>
                                        $("#chat-form").addClass("d-none");
                                    </script>
                                    `
                                )
                                submitButton.html('<i class="fa-solid fa-paper-plane"></i>');
                                submitButton.removeAttr("disabled")
                            }
                            if("is_on_progress" in jsonData && jsonData.is_on_progress){
                                var response_html = converter.makeHtml(jsonData.res)
                                $(`#response_${jsonData.message_id}`).html(response_html)
                            }
                            
                            $('#top').scrollTop($('#top')[0].scrollHeight);

                            // Process the JSON data (e.g., append to a DOM element)
                        } catch (error) {
                            console.error('Error parsing JSON:', error);
                            controller.error(error);
                        }
                        // Continue reading
                        read();
                    }).catch(error => {
                        console.error('Error reading response:', error);
                        controller.error(error);
                    });
                }
                
                // Start reading the response stream
                read();
            }
        });
        
        // Pipe the response stream to another stream or process it directly
        // For example, you can use a TransformStream to process the data
        // stream.pipeTo(someWritableStream);
    } else {
        // Handle non-streaming response (e.g., regular JSON response)
        return response.json().then(data => {
            console.log('Received non-streaming data:', data);
        });
    }
})
.catch(error => {
    console.error('Fetch error:', error);
});

});

//});


$('#id_message').on('input', function() {
    var text = $(this).val().trim(); 
    if (text === '') {
        $('#btn-submit').addClass('disabled');
    } else {
        $('#btn-submit').removeClass('disabled');
    }
});
function adjustChatContainer() {
    $("#chat-container").addClass("w-75");
    $(window).resize(function(){
        var viewportWidth = $(window).width();
        if (viewportWidth < 800){
            $("#chat-container").removeClass("w-75");
            $("#chat-container").addClass("w-100");
        }else{
            $("#chat-container").removeClass("w-100");
            $("#chat-container").addClass("w-75");
        }
    });
    $(window).resize();
}

// Call the function when the page loads
$(document).ready(function(){
    $('#id_message').focus();
    adjustChatContainer();
    $("#adjust-chat-button").click(function() {
        $('#top').animate({
        scrollTop: $('#top')[0].scrollHeight
    }, 'slow');        
    });
    // Add change event listener to the input field
    $('#id_image').change(function(event) {
        var file = event.target.files[0];
        // Create a URL for the selected file
        var imageURL = URL.createObjectURL(file);
        // Set the created URL as the src attribute of the img tag
        $('#uploaded-img').attr('src', imageURL);
        // Show the modal
        $('#id_message').attr('placeholder', 'Add text message (Optional)')
        $('#modal-uploaded-image').modal('show');

    });
    $('#btn-change').click(function() {
        // Trigger click event on the file input field to open file selection dialog
        $('#lbl-upload-image').click();
    });
    $('#clear-selection').click(function() {
        $('#uploaded-img').attr('src', '');
        $('#id_image').val('');
        $('#modal-uploaded-image').modal('hide');
        $('#id_message').attr('placeholder','Enter message');
        $('#id_message').focus();
    });
    $('#close-modal').click(function() {
        // Trigger click event on the file input field to open file selection dialog
        $('#id_message').focus();
    });
});



$(document).ready(function() {
    $('#top').animate({
        scrollTop: $('#top')[0].scrollHeight
    }, 'slow');
    $('#id_message').keypress(function(event) {
        // Check if the Enter key is pressed
        if (event.keyCode === 13 && !event.shiftKey) {
            event.preventDefault();
            $('#btn-submit').click();
        }
    });
});
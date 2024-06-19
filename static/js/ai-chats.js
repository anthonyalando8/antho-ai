
$(document).ready(function(){
    function get_element_height() {
        var new_height = $("#chat-form").outerHeight(true);
        return new_height;
    }

    function setSectionHeight(new_height){
        //return $(".top-section").height(new_height);
        console.log("newhight:" ,new_height)
        $(".top-section").css({
            "height": `calc(100% - ${new_height}px)`,
            "max-height": `calc(100% - ${new_height}px)`,
            "min-height": `calc(100% - ${new_height}px)`
        })
    }
    // Call the function once when the document is ready
    setSectionHeight(get_element_height())

    // Attach the function to the window resize event
    $(window).resize(function(){
        setSectionHeight(get_element_height())
    });
    var prompts_loader = document.getElementById("prompts-loader");
    var converter = new showdown.Converter();

    var user_avatar = "https://ik.imagekit.io/anthonyalando/Soft_Connect/user.png?updatedAt=1682239876486"
    var softchat_avatar = "https://ik.imagekit.io/anthonyalando/Soft_Connect/cpu.png?updatedAt=1715174298728"
    var converted_to_html_user_avatar_name = converter.makeHtml(`<div markdown="1" class="d-flex m-2 align-items-center flex-row my-2"><div markdown="1">![your image](${user_avatar} =32x32 "You")</div><div markdown="1" class="mx-md-3 mx-2">**You**</div></div>`)
    var converted_to_html_softchat_avatar_name = converter.makeHtml(`<div markdown="1" class="d-flex m-2 align-items-center flex-row my-2"><div markdown="1">![soft connect logo](${softchat_avatar} =32x32 "SoftChatAI")</div><div markdown="1" class="mx-md-3 mx-2"> **SoftChatAI**</div></div>`)
    
    var spinner = `
        <div class="spinner-grow text-light" role="status">
        <span class="visually-hidden">Loading...</span>
        </div>
        <div class="spinner-grow text-light" role="status">
        <span class="visually-hidden">Loading...</span>
        </div>
        <div class="spinner-grow text-light" role="status">
        <span class="visually-hidden">Loading...</span>
        </div>
    `
    var prompts = [
        "Suggest a unique recipe for a healthy breakfast.",
        "What's an interesting fact about space?",
        "Give me a motivational quote to start my day.",
        "What are the top three travel destinations in Europe?",
        "Explain the importance of mindfulness in daily life.",
        "Recommend a good book for a weekend read.",
        "Share a fun fact about ancient civilizations.",
        "How can I improve my productivity at work?",
        "What's a creative idea for a kid's birthday party?",
        "What are the principles of SOLID in software design?",
        "Explain the role of Docker in containerization.",
        "How do you handle authentication and authorization in a web app?",
        "Provide tips for maintaining a healthy work-life balance.",
        "Suggest a recipe for a unique and delicious dessert that would impress my friends at a dinner party?",
        "What are some creative theme ideas for a summer garden party that will keep guests entertained?",
        "Can you recommend some fun and unusual board games or party games that are great for large groups?",
        "What are some exciting and easy-to-make finger foods or snacks that would be perfect for a movie night with friends?",
        "Explain the concept of recursion in programming.",
        "How does the map function work in Python?",
        "What's the difference between let and var in JavaScript?",
        "How do you implement a binary search algorithm?",
        "Explain the Model-View-Controller (MVC) architecture.",
        "What are some best practices for writing clean code?",
        "Describe how to use Git for version control."
    ]
    var prompt_container = document.createElement("div")
    prompt_container.classList.add('row', 'g-3', "g-lg-4");
    prompts_loader.innerHTML= spinner;

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

                    //create a div elements
                    for (let i = prompts.length - 1; i > 0; i--) {
                        const j = Math.floor(Math.random() * (i + 1));
                        [prompts[i], prompts[j]] = [prompts[j], prompts[i]]; // Swap elements
                    }
                    // Return the first 'count' elements
                        prompts.slice(0, 4).forEach((element)=>{
                            var element_container = document.createElement('div');
                            element_container.classList.add("bg-dark", "text-light", "col-sm-12", "col-md-6", "col-xxl-3","p-2", "card");
                            element_container.style.cursor = "pointer"
                            element_container.innerHTML = element
                            element_container.addEventListener("click", function(){
                                $("#id_message").val(element)
                                $('#btn-submit').click()
                            });
                            prompt_container.appendChild(element_container)
                        })
                        prompts_loader.innerHTML=""
                    prompts_loader.appendChild(prompt_container)
                    // prompts_loader.classList.add('d-block')
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
                            image_html = converter.makeHtml(`<div markdown="1" style="max-width: 500px; max-height: 500px" class="m-2 overflow-hidden">![Image](${image})</div>`)
                        }
                        // Convert Markdown to HTML
                        var response_to_html = converter.makeHtml(response)
                        var response_ai_name = converted_to_html_softchat_avatar_name+`<div class="ml-2 m-2" >${response_to_html}</div>`;
                        var message_user_name = converted_to_html_user_avatar_name + `<div class="ml-2 m-2">${image_html}${message}</div>`;
                        htmlData += (message_user_name+response_ai_name)
                        chathistory = element.fields.chatHistory
                    });
                    prompts_loader.innerHTML = ""
                    prompts_loader.classList.add('d-none')

                    $("#chat").html(htmlData)
                    hljs.highlightAll()
                    
                    $("#get_ai_chats").attr("value", chathistory)
                    console.log($("#get_ai_chats").attr("value"))

                } catch (error) {
                    console.error("Error parsing JSON:", error);
                    prompts_loader.innerHTML = ""
                    prompts_loader.classList.add('d-none')

                    createToast("Error loading previous chat!", -1)

                }
               
            },
            error: function(error){
                console.log(error)
                prompts_loader.innerHTML = ""
                prompts_loader.classList.add('d-none')

                createToast("Error retrieving history!", -1)

            }
        });

    });

    //create a socket connection

    let session_id = $("#user_session_id").val();
    var submitButton = $('#form button[type="submit"]');

    connectWebSocket();
    function connectWebSocket(){
        try{
            //check the current protocol used https or http
            var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
            var chat_socket = new ReconnectingWebSocket(
                `${ws_scheme}://`
                    + window.location.host
                    + `/${ws_scheme}/chat/`
                    + session_id
                    + '/',
                    null,
                    {maxReconnectAttempts: 5, reconnectInterval: 5550}
            )
            
            chat_socket.onopen = function(e){
                createToast("Secure connection established.", 200)
                //retrieve user previous messages
                $("#btn_get_chats").click();
                //display the chat container with form
                $("#chat-form").removeClass("d-none");
                sendSeverMessage(chat_socket);
                //adjust chat body height
                setSectionHeight(get_element_height());
            }

            
            //when a message is received from the server side
            chat_socket.onmessage = function(e){
                handleReceivedMessages(e.data)
            }
        
            chat_socket.onclose = function(e){
                $("#chat-form").addClass("d-none");
                //adjust chat body height
                createToast("Server connection closed!", -1)
                setSectionHeight(get_element_height());
                console.log("Server closed unexpectedly: ", e)
            }
            
            
        }catch(error){
            $("#chat-container").addClass("d-none");
        }
    }

    function sendSeverMessage(chat_socket){
        // Add an event listener to the form submission
        const form = document.getElementById('form');
        form.addEventListener('submit', async function(event) {
            // Prevent the default form submission

            event.preventDefault();
            
            
            // Create a FormData object and populate it with form data
            const dataForm = new FormData(form);
    
            var formObject = {}
            // Function to convert file to Base64
            function fileToBase64(file) {
                return new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.readAsDataURL(file);
                    reader.onload = () => resolve(reader.result);
                    reader.onerror = error => reject(error);
                });
            }
            for (let [key, value] of dataForm.entries()) {
                if (value instanceof File && value != null && value.size > 0) {
                    formObject[key] = await fileToBase64(value);
                } else {
                    formObject[key] = value;
                }
            }
            $('#form')[0].reset();
            
            try{
                chat_socket.send(JSON.stringify({
                    'message_content': formObject
                }))

                $("#prompts-loader").html("")

                $('#btn-submit').addClass('disabled');

                submitButton.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
                submitButton.attr("disabled","disabled");
            }catch(error){
                createToast("No server connection! Reload page", -1)
            }
            
        });
    }

    function handleReceivedMessages(server_message){
        try {
            //hide the prompts loader
            prompts_loader.classList.add('d-none')
            // Parse the string as JSON
            const jsonData = JSON.parse(server_message);
            if("is_first" in jsonData && jsonData.is_first){
                $("#chat").append(converted_to_html_user_avatar_name+`<div class="m-2">${jsonData.prompt}</div>`)

                if(jsonData.image != null){
                    var image_tag = document.createElement("img");
                    image_tag.classList.add("img-fluid");
                    image_tag.style.maxHeight = "400px";
                    image_tag.setAttribute('src', jsonData.image)
                }
                $("#chat").append(image_tag);
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
                            ${jsonData.error_message} <a href="/chat/" class="alert-link">Reload</a>
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

            if('is_done' in jsonData && jsonData.is_done){
                submitButton.html('<i class="fa-solid fa-paper-plane"></i>');
                submitButton.removeAttr("disabled")
                $('#id_message').attr('placeholder','Enter message');
                $('#id_message').focus();
            }
            hljs.highlightAll()
            $('#top').scrollTop($('#top')[0].scrollHeight);

            // Process the JSON data (e.g., append to a DOM element)
        } catch (error) {
            console.error('Error parsing JSON:', error);
            createToast("Error appending response!", -1)
            hljs.highlightAll()
        }
    }

    $('#top').animate({
        scrollTop: $('#top')[0].scrollHeight
    }, 'slow');
    $('#id_message').keypress(function(event) {
        // Check if the Enter key is pressed
        if (event.keyCode === 13 && !event.shiftKey) {
            event.preventDefault();
            if($("#id_message").val().length != 0)
                $('#btn-submit').click();
        }
    });

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
        // when the modal is closed message input field achieve focus
        $('#id_message').focus();
    });
});


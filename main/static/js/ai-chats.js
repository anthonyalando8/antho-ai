
$(document).ready(function(){

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
                    var user_avatar = "https://ik.imagekit.io/anthonyalando/Soft_Connect/user.png?updatedAt=1682239876486"
                    var softchat_avatar = "https://ik.imagekit.io/anthonyalando/Soft_Connect/cpu.png?updatedAt=1715174298728"
                    var htmlData = ""
                    var converter = new showdown.Converter();
                    var converted_to_html_user_avatar_name = converter.makeHtml(`<div markdown="1" class="d-flex align-items-center flex-row my-2"><div markdown="1">![your image](${user_avatar} =32x32 "You")</div><div markdown="1" class="mx-md-3 mx-2">**You**</div></div>`)
                    var converted_to_html_softchat_avatar_name = converter.makeHtml(`<div markdown="1" class="d-flex align-items-center flex-row my-2"><div markdown="1">![soft connect logo](${softchat_avatar} =32x32 "SoftChatAI")</div><div markdown="1" class="mx-md-3 mx-2"> **SoftChatAI**</div></div>`)
                    var chathistory = "new_chat"
                    jsonData.forEach(element => {
                        var message = element.fields.message;
                        var response = element.fields.response;
                        var image = element.fields.image;
                        // Create a Showdown converter
                        var image_html = ""
                        
                        if(image != null && image != ""){
                            image_html = converter.makeHtml(`<div markdown="1" style="max-width: 500px; max-height: 500px" class"overflow-hidden">![Message Image](${image})</div>`)
                        }
                        // Convert Markdown to HTML
                        var response_to_html = converter.makeHtml(response)
                        var response_ai_name = converted_to_html_softchat_avatar_name+`<div class="ml-2">${response_to_html}</div>`;
                        var message_user_name = converted_to_html_user_avatar_name + `<div class="ml-2">${image_html}${message}</div>`;
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

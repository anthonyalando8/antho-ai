
$(document).ready(function(){
    //Sending reply to server
    function submit_reply(form, modal_close_btn){
        form.addEventListener("submit", async function(event){
            event.preventDefault()
            var formData = new FormData(form)
            var submitButton = $(form).find('button[type="submit"]');

                // Now you can do something with the submit button, for example, disable it
            submitButton.prop('disabled', true);
            submitButton.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span');
            fetch(form.getAttribute("action"),{
                method: "POST",
                body: formData
            }).then(response =>{
                return response.json()             
            }).then(data =>{
                var status_code = data.status_code;
                var messages = data.message;
                var status_message = "";
                $.each(messages, function(key, value) {
                    status_message += value
                });
                submitButton.prop('disabled', false);
                submitButton.html('Send Reply');
                modal_close_btn.click()
                createToast(status_message, status_code == "ok" ? 200 : -1)
                $("#btn-get-messages").click()                
            })
            .catch(error =>{
                console.log(error)
                createToast("Not sent. Try again Later!", -1)
                submitButton.prop('disabled', false);
                submitButton.html('Send Reply');
            })
        });
    }


    function createModalForm(message_obj, modal_close_btn){
        var form_container = document.createElement("div");
        var message_view = document.createElement("div");
        message_view.classList.add("row", "g-2")
        form_container.classList.add("p-2","border", "border-light", "rounded");
        [
            { key: "Reference Code: ", value: message_obj.fields.message_reference_code },
            { key: "Email: ", value: message_obj.fields.email },
            { key: "Subject: ", value: message_obj.fields.message_subject },
            { key: "Date: ", value: message_obj.fields.date },
            { key: "Phone: ", value: message_obj.fields.phone },
            { key: "Answered: ", value: message_obj.fields.is_responded },
            { key: "Marked urgent: ", value: message_obj.fields.is_urgent},
            { key: "Message: ", value: message_obj.fields.message_body}
        ].forEach(attr =>{
            var message_element_label = document.createElement("div");
            message_element_label.classList.add("col-12","col-md-4", "col-xxl-3", "p-1", "text-break", "fw-bold")
            message_element_label.innerText = attr.key;
            var message_element_value = document.createElement("div");
            message_element_value.classList.add("col-12","col-md-8", "col-xxl-9", "p-1", "border", "border-light", "rounded", "text-break")
            message_element_value.innerText = attr.value;
            message_view.appendChild(message_element_label);
            message_view.appendChild(message_element_value);

        })
        var reply_form = document.createElement("form");
        reply_form.classList.add("form");
        reply_form.setAttribute("method", "post")
        reply_form.setAttribute("action", "/manage/admin/messages")
        var csrf_token_field = document.createElement("input")
        csrf_token_field.setAttribute("type", "hidden");
        csrf_token_field.setAttribute("name", "csrfmiddlewaretoken")
        var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        csrf_token_field.setAttribute("value", csrf_token)
        
        var form_floating = document.createElement("div");
        var hidden_send_reply = document.createElement("input");
        hidden_send_reply.setAttribute("name","send_reply")
        hidden_send_reply.setAttribute("value", "true");
        hidden_send_reply.setAttribute("type", "hidden");
        hidden_send_reply.setAttribute("id", "send_reply");
        var hidden_message_code = document.createElement("input");
        hidden_message_code.setAttribute("name","message_reference_code")
        hidden_message_code.setAttribute("value", message_obj.fields.message_reference_code);
        hidden_message_code.setAttribute("type", "hidden");
        hidden_message_code.setAttribute("id", "message_reference_code");
        form_floating.classList.add("form-floating", "mt-2");
        var text_area = document.createElement("textarea");
        text_area.classList.add("form-control");
        text_area.style.height = "150px";
        text_area.setAttribute("id", "message_reply");
        text_area.setAttribute("name", "message_reply")
        var text_area_label = document.createElement("label");
        text_area_label.setAttribute("for", "message_reply");
        text_area_label.innerText = "Enter Message";
        var btn_submit_reply = document.createElement("button");
        btn_submit_reply.setAttribute("type", "submit");
        btn_submit_reply.setAttribute("id","btn_submit_reply");
        btn_submit_reply.classList.add("btn", "btn-success", "mt-2");
        btn_submit_reply.innerText = "Send Reply";
        
        submit_reply(reply_form, modal_close_btn);

        form_floating.appendChild(text_area);
        form_floating.appendChild(text_area_label);
        reply_form.appendChild(csrf_token_field);
        reply_form.appendChild(hidden_send_reply);
        reply_form.append(hidden_message_code);
        reply_form.appendChild(form_floating);
        reply_form.appendChild(btn_submit_reply);
        form_container.appendChild(message_view);
        form_container.appendChild(reply_form);
        return form_container
    }
    function showModal(message_obj){
        //$('#modal-view-message').modal('show')
        var modal = document.createElement("div");

        modal.classList.add("modal", "fade");
        const createAndSetAttributes = (element, attributes) => {
            attributes.forEach(attr => {
                element.setAttribute(attr.key, attr.value);
            });
        };
        createAndSetAttributes(modal, [
            { key: "id", value: "modal-view-message" },
            { key: "data-bs-backdrop", value: "static" },
            { key: "data-bs-keyboard", value: "true" },
            { key: "tabindex", value: "-1" },
            { key: "aria-labelledby", value: "modal-uploaded-view-message-label" },
            { key: "aria-hidden", value: "true" }
        ]);
    
        var modal_dialog = document.createElement("div");
        modal_dialog.classList.add("modal-dialog", "modal-xl","modal-dialog-centered", "modal-dialog-scrollable")
    
        var modal_content = document.createElement("div")
        modal_content.classList.add("modal-content")
        var modal_header = document.createElement("div")
        modal_header.classList.add("modal-header")
        var modal_title = document.createElement("div");
        modal_title.classList.add("modal-title", "h1", "fs-5");
        modal_title.innerHTML = `From: <span>${message_obj.fields.user_name}</span>` 
        var modal_close_btn = document.createElement("button");
        modal_close_btn.classList.add("btn-close");
        createAndSetAttributes(modal_close_btn, [
            { key: "type", value: "button" },
            { key: "data-bs-dismiss", value: "modal" },
            { key: "aria-label", value: "Close" }
        ]);
        modal_close_btn.addEventListener('click', function(){
            modal.remove()
        })
        var modal_body = document.createElement("div");
        modal_body.classList.add("modal-body")
        modal_body.appendChild(createModalForm(message_obj, modal_close_btn))
        var modal_footer = document.createElement("div")
        modal_footer.classList.add("modal-footer")
        
        
        modal_header.appendChild(modal_title)
        modal_header.appendChild(modal_close_btn)
        modal_content.appendChild(modal_header)
        modal_content.appendChild(modal_body)
        modal_content.appendChild(modal_footer)
        modal_dialog.appendChild(modal_content)
        modal.appendChild(modal_dialog)
        document.body.appendChild(modal)

        $('#modal-view-message').modal('show')

    }


    $('#form-get-messages').submit(function(event){
        event.preventDefault();

        var formData = new FormData(this);

        var table_container = document.createElement('div');
        table_container.classList.add('table-responsive-md');
        var table = document.createElement('table');
        table.classList.add('table');
        table.classList.add('table-striped');
        table.classList.add('table-hover');
        var table_head = document.createElement('thead');
        var table_row_head = document.createElement('tr');
        ["#", "Sender","Email", "Message", "Answered"].forEach(function(value){
            var th = document.createElement('th');;
            th.setAttribute('scope','col');
            th.innerHTML = value;
            table_row_head.appendChild(th);
        });

        table_head.append(table_row_head)
        table.appendChild(table_head)
        var table_body = document.createElement("tbody");
        $("#main").html("Refreshing...");

 
        if (formData && formData.entries().next().done === false) {
            $.ajax({
                type: "POST",
                url: $(this).attr('action'),
                data: formData,
                processData: false,
                contentType: false,
                success: function(response){
                    var jsonData = JSON.parse(response);
                    jsonData.forEach(function(obj) {
                        // Access fields of each object
                        var table_row_body = document.createElement("tr");
                        var td_id = document.createElement("td");
                        
                        td_id.innerHTML = obj.pk;
                        
                        table_row_body.appendChild(td_id);
                        var td_user = document.createElement("td");
                        td_user.innerHTML = obj.fields.user_name;
                        td_user.classList.add("truncate");
                        table_row_body.appendChild(td_user)
                        var td_email = document.createElement("td");
                        td_email.innerHTML = obj.fields.email;
                        td_email.classList.add("truncate")
                        table_row_body.appendChild(td_email);

                        var td_message_body = document.createElement("td");
                        td_message_body.classList.add("truncate");
                        td_message_body.innerHTML = obj.fields.message_body;
                        table_row_body.appendChild(td_message_body);

                        var td_answered = document.createElement("td");
                        td_answered.innerHTML = obj.fields.is_responded ? "Answered" : "Pending";

                        table_row_body.style.cursor = "pointer";
                        table_row_body.addEventListener('click', function(){
                            showModal(obj);
                        })
                        table_row_body.appendChild(td_answered);
                        table_row_body.classList.add(obj.fields.is_urgent ? "table-danger" : "table-row");
                        table_body.appendChild(table_row_body);
                    }); 
                    table.appendChild(table_body)
                    table_container.appendChild(table);
                    $("#main").html(table_container);
                    $("#badge-message-count").html(jsonData.length)

                },
                error: function(error){
                    console.log(error)
                }
            })
        }else{
            console.log("FormData is empty");
        } 
    });
    $('#btn-get-messages').click();
})

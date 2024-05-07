function showModal(message_obj){
    $('table-messages').append(`{% block modaltitle %} Subject {% endblock %}{% modalbody %}Message{% endblock %}`)
    $('#modal-view-message').modal('show')
}
$(document).ready(function(){
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
        var table_row_head = document.createElement('tr');;
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
                    console.log(jsonData);
                    jsonData.forEach(function(obj) {
                        // Access fields of each object
                        console.log(obj.fields.user);
                        console.log(obj.fields.email);
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

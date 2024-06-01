// $(document).ready(function(){
//     function retrieve_notification(){
//         const formData = new FormData();
//         var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
//         formData.append("gan", "true");
//         formData.append("csrfmiddlewaretoken", csrf_token)

//         fetch("/manage/admin/dashboard", {
//             method: "POST",
//             body: formData,
//         })
//         .then(response => {
//             return response.json()
//         }).then(data =>{
//             if (Object.keys(data).length === 0 && data.constructor === Object) {
//                 console.log("Data is empty");
//             }
//             console.log(data)
//             // let response_code = data.status_response.status_code
//             // let response_message = data.status_response.status_text
//             // if(response_code == "ok"){
//             //     let unread_responses = data.unread_response_count;
//             //     let messages = data.messages;
//             //     if(unread_responses > 0){
//             //         $("#fa-bell-notification").addClass("fa-shake");
//             //         $("#btn-bell-notification").addClass("text-danger")
//             //         $("#notification-badge").removeClass("d-none")
//             //         $("#btn-bell-notification").addClass("text-warning")
//             //         $("#notification-badge").text(unread_responses > 99 ? "99+": unread_responses)
//             //     }else{
//             //         $("#notification-badge").addClass("d-none")
//             //         $("#btn-bell-notification").addClass("text-light")
//             //     }
//             //     if (messages.length > 0){
//             //         console.log("user has messages")
//             //     }else{
//             //         console.log("user has no messages")
//             //     }
                
//             // }else{
//             //     console.log("Error received")
//             //     $("#btn-bell-notification").addClass("text-light")
//             // }
            
//         })
//         .catch(error => {
//             console.error("Error submitting form:", error);
//         });

//     }
//     retrieve_notification()
// })

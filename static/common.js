document.addEventListener('DOMContentLoaded', function () {
    var messages = document.querySelectorAll(".alert")

    messages.forEach(function (message) {
        setTimeout(function () {
            message.style.display = 'none';
        }, 4000);
    });

    // document.addEventListener('click', function(event) {
    //     closeUserDetailsPopup();
    // });
   
});


document.getElementById('backButton').addEventListener('click', function() {
    event.preventDefault(); 
    window.history.back();
});
document.getElementById('searchEmp').addEventListener('keydown', function() {
    if (event.key === 'Enter') {
        event.preventDefault();
        // fetch('/search', { method: 'GET' })
        //     .then((result) => {
        //         console.log('Flask route called successfully', result);
        //         window.location.href = '/search';
        //     })
        //     .catch(error => {
        //         console.error('Error calling Flask route:', error);
        //     });
    }
});

function showUserDetails() {
    fetch('/get_user_details')
    .then(response => response.json())
    .then(data => {
        document.getElementById('user-details-content').innerHTML = 'User ID: ' + data[0] + '<br>' +
        'Username: ' + data[1];
        document.getElementById('user-details-popup').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
    });

}

function closeUserDetailsPopup() {
    document.getElementById('user-details-popup').style.display = 'none';
}

function showPasswordFunction(id) {
    var x = document.getElementById(id)
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
} 

// function showNotification(category, message) {
//     var notificationBar = document.getElementById('notification-bar');
//     notificationBar.innerHTML = message;
//     notificationBar.style.backgroundColor = getCategoryColor(category);
//     notificationBar.style.display = 'block';

//     // Hide the notification after 3 seconds (adjust as needed)
//     setTimeout(function() {
//         notificationBar.style.display = 'none';
//     }, 3000);
//  }


// function showBtn(){
   
//     setTimeout(function() {
//         document.getElementById('clear-button').style.display = 'block';
//             }, 1000);
// }

document.addEventListener('DOMContentLoaded', function(){

    function getCookie(name){
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if(parts.length == 2) return parts.pop().split(';').shift();
    }
   
    // Create new post Dialog Modal 
    const newPostModal = document.querySelector("[data-modal]");
    const openButton = document.querySelector("[data-open-modal]");
    const closeButton = document.querySelector(".close-modal");
   
   // Add event listener to  open new post modal 
    openButton.addEventListener("click", function(e) {
        e.preventDefault();
        newPostModal.showModal();
     });

   
   //  close New post modal 
   closeButton.addEventListener('click', ()=>{
    console.log('I am clicked');
    newPostModal.close();
   })
 

//  To close modal on every side 
 newPostModal.addEventListener("click", function(e) {
         const dialogDimensions = newPostModal.getBoundingClientRect()
        if (
          e.clientX < dialogDimensions.left ||
          e.clientX > dialogDimensions.right ||
           e.clientY < dialogDimensions.top ||
           e.clientY > dialogDimensions.bottom
         ) {
           newPostModal.close()
         }
      })
      // END OF CREATE NEW POST MODAL 
      // ========================================



      // Create a new Post in JavaScript 

      const newPost = document.querySelector('.js-submit');
      
      
     newPost.addEventListener('click', (e) => {
        e.preventDefault();
        createNewPost();
     })


  // new post API
     function createNewPost(){   
        const textareaValue = document.querySelector('.js-post-text').value;
        const url = `http://localhost:8000/api/post-create/`;
        const options = {
            method: "POST",
            headers: {
                "Content-type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({
                text: textareaValue,
            }),
        }

        fetch(url, options)
        .then((response) => response.text())
        .then((html) => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, "text/html");
            const post_list_dom = document.querySelector(".posts-container");
            // add doc as the first child in the post_list_dom

            if (post_list_dom !== null) {
                if (post_list_dom.innerHTML === "") {
                    window.location.href = 'http://localhost:8000/';
                } else {
                    post_list_dom.innerHTML = doc.body.innerHTML + post_list_dom.innerHTML;
                }
            } else {
                // Handle the case when post_list_dom is null
                console.error('post_list_dom is null');
            }
              
            newPostModal.close();
            document.querySelector('.js-post-text').value = '';
            location.reload()  
          })
        .catch((error) => {
            // Handle any errors that occur during the request
            console.error('Error creating a new post:', error);
          });
     }


      // to get data from form

    $.ajaxSetup({
        beforeSend: function beforeSend(xhr, settings) {
            function getCookie(name) {
                let cookieValue = null;
    
    
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
    
                    for (let i = 0; i < cookies.length; i += 1) {
                        const cookie = jQuery.trim(cookies[i]);
    
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
    
                return cookieValue;
            }
    
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            }
        },
    });
    
    
    //  Make new post with JavaScript. 



  


// Follow and Unfollow 

$(document).on('click', '.js-follow', function(e){
    e.preventDefault();
    action = $(this).attr('data-action')
   
    $.ajax({
        type: 'POST',
        url: $(this).data("url"),
        data: {
            action: action,
            username: $(this).data('username'),
        },
        success: (data) => {
            console.log(data.total_followers)
            $('.js-follow-text').text(data.wording)

            // Update follower count
            $('.follower-count').text(data.total_followers);


             if(action == "follow") {
                // change the word to unfollow
                $(this).attr("data-action", "unfollow")
               

            }else{
                // The opposite
                $(this).attr("data-action", "follow")    
                $('.follower-count').text(data.total_followers);

            }
            
        },
        error: (error) => {
            console.warn(error)
            
        }
    });



})




// ==============================================================
// I want to use Javascript instead of JQuery for my like  and Unlike 
//=====================================================================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Begins code 





const likeButtons = document.querySelectorAll('.like-button');

likeButtons.forEach(button => {
    button.addEventListener('click', async (e) => {
        e.preventDefault();
        const postId = button.getAttribute('data-post-id');
   
        // Additional logic to handle liking the post using postId...

        const url = `http://localhost:8000/likes/${postId}/`;
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken // 
            },
            body: JSON.stringify({ post_id: postId }),
        };

        try {
            const response = await fetch(url, options);

            if (response.ok) {
               
                // Handle UI changes or additional logic for successful like
                const data = await response.json(); // Parse the JSON response
                
                let action = data.status;

                if (action === 'liked' ){
                    
                    button.innerHTML = '&#10084;'
                    
                    countLikes()
                    postLikesCount()
 
                 } else if (action === 'unliked'){
                    
                    button.innerHTML = '&#9829; '
                    countLikes()
                    postLikesCount()
                   
                 }
        
            } else {
                throw new Error('Network response was not ok');
            }
        } catch (error) {
            console.error('There was an error:', error);
        }
    });
});


function countLikes() {
    const likeCountElements = document.querySelectorAll('.like-count');
    
    likeCountElements.forEach(countElement => {
        const postId = countElement.getAttribute('data-count-id'); // Assuming post ID is stored in a data attribute
             
         
        
        const url = `like_count/${postId}/`;
        const options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        };
            
        fetch(url,options)
        .then(response => response.json())
        .then(data => {
            
            // Update the UI with the received like count
            countElement.innerHTML = data.likeCount;
        })
        .catch(error => console.log(error));

        
    });
}

countLikes();


function postLikesCount(){
    const postLikeCounts = document.querySelectorAll('.like-detail-count');

     postLikeCounts.forEach(postLikes => {
        const postId = postLikes.getAttribute('data-detail-count-id');
        const url = `/like_counts/${postId}/`;

        const options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        };

        fetch(url, options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            postLikes.innerHTML = data.likeCounts
            console.log(data.likeCounts);
            // Process the received data
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            // Handle the error (e.g., display a message to the user)
        });
    

     })
    
}

postLikesCount()









});










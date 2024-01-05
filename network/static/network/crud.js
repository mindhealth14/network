const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();

}
const openEditModal = (button) => {
    const post_id = button.getAttribute('data-postId')
    const post_text = document.querySelector(`#post-content-${post_id}`).innerText
    const editModal = document.querySelector("[data-update-modal]");
    const updateModalTextArea = document.querySelector("#js-update-post-id-textarea")
    updateModalTextArea.value = post_text
    const updateModalPostId = document.querySelector("#js-update-post-id-hidden")
    updateModalPostId.value = post_id
    editModal.showModal()
};

const closeEditModal = () => {
    // clean up
    const updateModalTextArea = document.querySelector("#js-update-post-id-textarea")
    updateModalTextArea.value = ""
    const updateModalPostId = document.querySelector("#js-update-post-id-hidden")
    updateModalPostId.value = ""
    const editModal = document.querySelector("[data-update-modal]");
    editModal.close()
};

const handlePostUpdate = async () =>{
    const text = document.querySelector("#js-update-post-id-textarea").value
    const postId = document.querySelector("#js-update-post-id-hidden").value

    const req = await fetch(`http://localhost:8000/api/post-update/${postId}/`, {
        method: "PUT",
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({text})
    }) 
    if (req.status === 200){
        const postContent = document.querySelector(`#post-content-${postId}`)
        postContent.innerText = text
        closeEditModal()
    }
    else{
        alert("Something went wrong")
    }
};

// DELETE
const openDeleteModal = (button) => {
    const post_id = button.getAttribute('data-postId')
    const delModal = document.querySelector("[data-delete-modal]");
    const delModalPostId = document.querySelector("#delete-id-broadcast")
    delModalPostId.innerText = post_id

    
    delModal.showModal()
};

const closeDeleteModal = () => {
    // clean up
    const delModalPostId = document.querySelector("#delete-id-broadcast")
    delModalPostId.innerText = ""
    const delModal = document.querySelector("[data-delete-modal]");
    delModal.close()
};

const handlePostDelete = async () =>{
    const postId = document.querySelector("#delete-id-broadcast").innerText
    const req = await fetch(`http://localhost:8000/api/post-delete/${postId}/`, {
        method: "DELETE",
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
    }) 
    if (req.status === 200){
        const post = document.querySelector(`#post-container-${postId}`)
        post.remove()
        closeDeleteModal()
    }
    else{
        alert("Something went wrong")
    }
};

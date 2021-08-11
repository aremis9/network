
document.addEventListener("DOMContentLoaded", () => {
    var followbtn = document.querySelector('#followbtn')
    if (followbtn !== null) {
        
        followbtn.addEventListener('click', () => {
            var action = ''
            if (followbtn.innerHTML == 'Follow') {
                followbtn.classList.remove('btn-primary')
                followbtn.classList.add('btn-secondary')
                followbtn.innerHTML = 'Unfollow'
                action = 'follow'
            }
            else {
                followbtn.classList.remove('btn-secondary')
                followbtn.classList.add('btn-primary')
                followbtn.innerHTML = 'Follow'
                action = 'unfollow'
            }

            // var csrf = 
            
            var user = document.querySelector('#user').innerHTML

            fetch(`/follow/${user}`, {
                method: 'POST',
                body: JSON.stringify({
                    action: action,
                })
            })
        })
        
    }

})


function editpost(id) {
    var post = document.querySelector(`#post${id}`)
    post.querySelector('#post-content').style.display = 'none'
    post.querySelector('#editbtn').style.display = 'none'
    post.querySelector('#edit-area').style.display = 'block'
    post.querySelector('#edit-save').style.display = 'block'
    post.querySelector('#edit-area').value = post.querySelector('#post-content').innerHTML
}

function savepost(id) {
    var post = document.querySelector(`#post${id}`)
    var new_content = post.querySelector('#edit-area').value

    post.querySelector('#post-content').style.display = 'block'
    post.querySelector('#editbtn').style.display = 'block'
    post.querySelector('#edit-area').style.display = 'none'
    post.querySelector('#edit-save').style.display = 'none'

    fetch(`/editpost/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: new_content
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result.message)
        if (result.message == 'Post edited.') {
            post.querySelector('#post-content').innerHTML = result.new_content
        }
        else if (result.error) {
            alert(result.error)
        }
    })
}
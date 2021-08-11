
function follow() {
    var followbtn = document.querySelector('#followbtn')
    followbtn.addEventListener('click', () => {
        followbtn.classList.remove('btn-primary')
        followbtn.classList.add('btn-secondary')
        followbtn.innerHTML = 'Following'
    })
}



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
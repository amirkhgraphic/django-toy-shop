function clearReplyOn(){
    document.getElementById('id_submission_type').value = 'comment'
    document.getElementById('id_comment').value = 0
    document.getElementById('replyingOn').innerHTML = '';
    document.getElementById('replyingOn').classList.remove('alert')
}

function setReply(commentId, authorUsername) {
    const replyOn = document.getElementById('replyingOn')
    replyOn.classList.add('alert')
    document.getElementsByClassName('comment-template')[0].scrollIntoView({ behavior: 'smooth' });

    replyOn.innerHTML = `<span id="clear-reply" onclick="clearReplyOn()">&times; </span> Replying on ${authorUsername}'s comment`;
    document.getElementById('id_submission_type').value = 'reply'
    document.getElementById('id_comment').value = commentId;
}
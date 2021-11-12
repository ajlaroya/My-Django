function commentReplyToggle(parent_id) {
    const row = document.getElementById(parent_id);
    if (row.classList.contains('is-hidden')) {
        row.classList.remove('is-hidden');
    } else {
        row.classList.add('is-hidden');
    }
}

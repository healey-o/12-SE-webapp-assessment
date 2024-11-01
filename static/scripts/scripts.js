
// Function to detect if the user wants to create a new group
function detectNewGroup() {
    const groupSelect = document.getElementById('group-select');
    const newGroupInput = document.getElementById('new-group-input');

    if (groupSelect.value === 'new') {
        newGroupInput.style.display = 'block';
    } else {
        newGroupInput.style.display = 'none';
    }
}
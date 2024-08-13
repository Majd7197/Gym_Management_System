
function toggleCustomRoleInput() {
    var roleSelect = document.getElementById('role');
    var customRoleContainer = document.getElementById('custom-role-container');
    var customDescriptionContainer = document.getElementById('custom-description-container');
    if (roleSelect.value === 'custom') {
        customRoleContainer.style.display = 'block';
        customDescriptionContainer.style.display = 'block';
    } else {
        customRoleContainer.style.display = 'none';
        customDescriptionContainer.style.display = 'none';
    }
}

// function formatPhoneNumber(value) {
//     // Remove all non-digit characters
//     value = value.replace(/\D/g, '');

//     // Add spaces after the third and sixth digits
//     if (value.length > 3) {
//       value = value.slice(0, 3) + ' ' + value.slice(3);
//     }
//     if (value.length > 7) {
//       value = value.slice(0, 7) + ' ' + value.slice(7);
//     }

//     // Trim to a maximum of 12 characters (including spaces)
//     return value.slice(0, 12);
//   }
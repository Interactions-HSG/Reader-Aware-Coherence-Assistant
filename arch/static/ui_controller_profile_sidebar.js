const toggleSidebar = document.getElementById('toggleSidebar');
const sidebar = document.getElementById('sidebar');

toggleSidebar.addEventListener('click', () => {
sidebar.classList.toggle('hidden');
});

//// Define a variable to keep track of the selected profile
let selectedProfile = null;

// Event listener for profile selection
document.querySelectorAll('.profile-button').forEach((button) => {
  button.addEventListener('click', () => {
    selectedProfile = button.getAttribute('data-profile');
    // You can add visual cues or styling to indicate the selected profile, if needed
  });
});



document.addEventListener('click', (event) => {
if (!sidebar.contains(event.target) && !toggleSidebar.contains(event.target)) {
    sidebar.classList.add('hidden');
}
});

// Event listener for profile selection
document.querySelectorAll('.profile-button').forEach((button) => {
  button.addEventListener('click', () => {
    // Remove "selected" class from all buttons
    document.querySelectorAll('.profile-button').forEach((btn) => {
      btn.classList.remove('selected');
    });

    // Add "selected" class to the clicked button
    button.classList.add('selected');

    selectedProfile = button.getAttribute('data-profile');
    let id_txtBox = document.getElementById('personal_ids');
    if(!!id_txtBox) id_txtBox.value = button.getAttribute('data-personal_id') //when click, the id appears
  });
});


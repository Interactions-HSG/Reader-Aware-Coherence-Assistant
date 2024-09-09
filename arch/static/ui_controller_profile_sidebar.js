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
    __SEP__ = ','
    id = button.getAttribute('data-personal_id');
    let id_txtBox = document.getElementById('personal_ids');

    // [20240909: Multiselector]
    /** Instead of adding or removing the class, toggle it
      if(button.classList.contains('selected'))
        button.classList.remove('selected'); // remove the class
      else
        button.classList.add('selected'); // add the class
    */
    button.classList.toggle('selected');

    // Update the list of id's
    // Look throug all profile-buttons and take ids of button with the class
    // "selected"
    ids = ''
    document.querySelectorAll('.profile-button').forEach((btn) => {
      if(btn.classList.contains('selected') && btn.getAttribute('data-personal_id'))
        ids = ids + ',' + btn.getAttribute('data-personal_id');
    });
    // remove orphan separator at the begining
    re = new RegExp(String.raw`(^${__SEP__}*)`)
    ids = ids.replace(re, '')


    if(!!id_txtBox) id_txtBox.value = ids;

  /** [20240909] Old version
    // Remove "selected" class from all buttons
    document.querySelectorAll('.profile-button').forEach((btn) => {
      btn.classList.remove('selected');
    });

    // Add "selected" class to the clicked button
    button.classList.add('selected');

    selectedProfile = button.getAttribute('data-profile');
    //let id_txtBox = document.getElementById('personal_ids');
    if(!!id_txtBox) id_txtBox.value = button.getAttribute('data-personal_id') //when click, the id appears 
   */
  });
});


let profileDropdownList = document.querySelector(".profile-dropdown-list");
let btn = document.querySelector(".profile-dropdown-btn");

let classList = profileDropdownList.classList;

const toggle = () => classList.toggle("active");

window.addEventListener("click", function (e) {
    if (!btn.contains(e.target)) classList.remove("active");
});

const profileDropdownBtn = document.querySelector('.profile-dropdown-btn');

profileDropdownBtn.addEventListener('click', toggleCaption);

function toggleCaption() {
  profileDropdownBtn.classList.toggle('show-caption');
}

document.addEventListener('click', (event) => {
  const isClickInside = profileDropdownBtn.contains(event.target);
  if (!isClickInside) {
    profileDropdownBtn.classList.remove('show-caption');
  }
});
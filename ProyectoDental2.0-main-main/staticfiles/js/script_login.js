const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const main = document.getElementById('main');

signInButton.addEventListener('click', ()=>{
    main.classList.remove("right-panel-active");
});

signUpButton.addEventListener('click', ()=>{
    main.classList.add("right-panel-active");
});



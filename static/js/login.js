
const form = document.querySelector('form');
const username = document.querySelector('#username');
const password = document.querySelector('#password');
const loginBtn = document.querySelector('#login-btn');
const error = document.querySelector('.error');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  if (username.value === '' || password.value === '') {
    error.textContent = 'Please enter your username and password.';
  } else {
    form.submit();
  }
});

loginBtn.addEventListener('click', () => {
  error.textContent = '';
});



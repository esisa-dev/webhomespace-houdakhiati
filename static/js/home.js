document.addEventListener("DOMContentLoaded", function() {
    const logoutButton = document.querySelector('.logout button');
    logoutButton.addEventListener('click', () => {
      console.log("1");
      fetch('/logout', {
        method: 'GET'
      }).then(response => {
        window.location.href = '/';
      });
      console.log("2");
    });
  });

  
  const filesBtn = document.getElementById('filesBtn');
  const contentDiv = document.getElementById('FDS');
  
  filesBtn.addEventListener('click', () => {
    fetch('/files')
      .then(response => response.text())
      .then(data => {
        contentDiv.innerHTML = data;
      })
      .catch(error => {
        console.error(error);
      });
  });

  const dirsBtn = document.getElementById('dirsBtn');
  dirsBtn.addEventListener('click', () => {
    fetch('/dirs')
      .then(response => response.text())
      .then(data => {
        contentDiv.innerHTML = data;
      })
      .catch(error => {
        console.error(error);
      });
  });

  const spaceBtn = document.getElementById('spaceBtn');
  spaceBtn.addEventListener('click', () => {
    fetch('/space')
      .then(response => response.text())
      .then(data => {
        contentDiv.innerHTML = data;
      })
      .catch(error => {
        console.error(error);
      });
  });


  const downloadButton = document.getElementById("telechargement-button");
const messageDiv = document.getElementById("FDS");

downloadButton.addEventListener("click", async () => {
    const response = await fetch('/download');
    const message = await response.text();
    messageDiv.innerHTML = message;
});

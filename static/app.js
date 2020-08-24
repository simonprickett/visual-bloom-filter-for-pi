  window.onload = function () {
    const addButton = document.getElementById('addButton');
    const existsButton = document.getElementById('existsButton');

    addButton.onclick = async function (e) {
      alert('add');
      e.preventDefault();
    }

    existsButton.onclick = async function (e) {
      e.preventDefault();
      alert('exists!');
    }
  };
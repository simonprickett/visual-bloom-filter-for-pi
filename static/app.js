  window.onload = function () {
    const callBloomFilter = async function (element, isAdd) {
      // TODO call the filter...
      const result = true;

      if (isAdd) {
        document.getElementById('displayResult').innerHTML = `<strong>${element}</strong> was added to the Bloom filter.`;
      } else {
        document.getElementById('displayResult').innerHTML = `<strong>${element}</strong> ${result ? 'may be' : 'is not'} in the Bloom filter.`;
      }

      document.getElementById('elementText').value = '';
    };

    const buttonClicked = async function (e, isAdd) {
      e.preventDefault();

      const element = document.getElementById('elementText').value

      if (element.length === 0) {
        return;
      }
      
      callBloomFilter(element, isAdd);
    };

    document.getElementById('addButton').onclick = function (e) {
      buttonClicked(e, true);
    };

    document.getElementById('existsButton').onclick = function (e) {
      buttonClicked(e);
    };

    document.getElementById('resetButton').onclick = async function (e) {
      e.preventDefault();

      document.getElementById('displayResult').innerHTML = 'Filter reset.';
      document.getElementById('elementText').value = '';
    }
  };
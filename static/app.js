  window.onload = function () {
    const API_PREFIX = 'api';

    const getResult = async function(response) {
      const responseData = await response.json();
      return responseData.result;
    };

    const callBloomFilter = async function (element, isAdd) {
      // TODO POST if it is the exists button...
      const response = await fetch(`/${API_PREFIX}/${isAdd ? 'add' : 'exists'}/${element}`);

      if (response.status !== 200  && response.status !== 201) {
        document.getElementById('displayResult').innerHTML = `Error calling backend :(`;
        return;
      }

      const result = await getResult(response);

      if (isAdd) {
        document.getElementById('displayResult').innerHTML = `<strong>${element}</strong> was ${result ? '' : 'not '}added to the Bloom filter.`;
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

      // TODO POST to the backend...

      document.getElementById('displayResult').innerHTML = 'Filter reset.';
      document.getElementById('elementText').value = '';
    }
  };
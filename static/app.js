  window.onload = function () {
    const API_PREFIX = 'api';

    const displayErrorCallingBackendMessage = function () {
      document.getElementById('displayResult').innerHTML = `Error calling backend :(`;
    };

    const getResult = async function(response) {
      const responseData = await response.json();
      return responseData.result;
    };

    const callBloomFilter = async function (element, isAdd) {
      const response = await fetch(`/${API_PREFIX}/${isAdd ? 'add' : 'exists'}/${element}`, { method: isAdd ? 'POST' : 'GET'});

      if (response.status !== 200  && response.status !== 201) {
        displayErrorCallingBackendMessage();
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
        document.getElementById('displayResult').innerHTML = '<strong>Enter a value then press Add or Exists.</strong>';
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
     
      document.getElementById('elementText').value = '';

      const response = await fetch(`/${API_PREFIX}/reset`, { method: 'POST' });

      if (response.status !== 200) {
        displayErrorCallingBackendMessage();
        return;
      }

      const result = await getResult(response);

      document.getElementById('displayResult').innerHTML = `Filter reset${result ? '' : ' failed'}.`;
    }
  };
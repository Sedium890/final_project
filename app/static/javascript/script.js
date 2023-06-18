const phoneInput = document.getElementById('phoneInput');

phoneInput.addEventListener('input', formatPhoneNumber);

function formatPhoneNumber() {
  const input = phoneInput.value.replace(/\D/g, ''); // Remove non-digit characters
  const areaCode = input.substring(0, 3);
  const firstPart = input.substring(3, 6);
  const secondPart = input.substring(6, 10);

  let formattedPhoneNumber = '';

  if (input.length > 6) {
    formattedPhoneNumber = `(${areaCode}) ${firstPart}-${secondPart}`;
  } else if (input.length > 3) {
    formattedPhoneNumber = `(${areaCode}) ${firstPart}`;
  } else if (input.length > 0) {
    formattedPhoneNumber = `(${areaCode}`;
  }

  phoneInput.value = formattedPhoneNumber;
}

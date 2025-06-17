// Load trains
fetch('/trains')
  .then(res => res.json())
  .then(trains => {
    const tbody = document.querySelector('#trains-table tbody');
    trains.forEach(train => {
      const row = `
        <tr>
          <td>${train.name}</td>
          <td>${train.source}</td>
          <td>${train.destination}</td>
          <td>${train.departure_time}</td>
          <td>${train.arrival_time}</td>
          <td>${train.id}</td>
        </tr>
      `;
      tbody.innerHTML += row;
    });
  });

// Handle booking
document.getElementById('booking-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const passengerName = document.getElementById('passengerName').value;
  const trainId = document.getElementById('trainId').value;

  fetch('/book', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      passenger_name: passengerName,
      train_id: trainId
    })
  })
  .then(res => res.json())
  .then(data => {
    alert(data.message);
    document.getElementById('booking-form').reset();
  });
});

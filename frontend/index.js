document.addEventListener('DOMContentLoaded', () => { // Wrap everything in DOMContentLoaded

  const registerForm = document.getElementById('register-form')
  const loginForm = document.getElementById('login-form')
  const formsContainer = document.querySelector('.forms')
  const content = document.querySelector('.content')

  // Funzioni di visibilità
  function showLogin() {
    formsContainer.hidden = false
    loginForm.hidden = false
    registerForm.hidden = true
    content.hidden = true
  }

  function showRegister() {
    formsContainer.hidden = false
    registerForm.hidden = false
    loginForm.hidden = true
    content.hidden = true
  }

  function showContent() {
    formsContainer.hidden = true
    loginForm.hidden = true
    registerForm.hidden = true
    content.hidden = false
  }

  function pushVotesData(array, dataType) {
    document.querySelectorAll(`.item-row-${dataType}`).forEach(row => {
      const input = row.querySelector('input')

      if (input.value) {
        array.push(parseInt(input.value))
      } else {
        array.push(0)
      }
    })
  }

  function appendDataToHtml(data, tableEl, list) {
    tableEl.innerHTML = '' // pulisce la tabella prima

    data.nome.forEach((nome, index) => {
      const tr = document.createElement('tr')

      // colonna nome
      const tdNome = document.createElement('td')
      tdNome.textContent = list[nome]
      tr.appendChild(tdNome)

      // colonna valore
      const tdValore = document.createElement('td')
      tdValore.textContent = data.valori[index] ?? 0
      tr.appendChild(tdValore)

      tableEl.appendChild(tr)
    })
  }

  // Funzione specifica per fare append di valori e non oggetti:
  // Risolve problemi con le tabelle dei "vincitori"
  function appendStandingsToTable(valuesArray, tableElement, labelsArray) {
    // 1. Svuota la tabella (evita che i dati si accumulino se clicchi più volte)
    tableElement.innerHTML = '';

    // 2. Cicla usando l'array delle etichette (nomi ristoranti o date)
    labelsArray.forEach((label, index) => {
        const row = document.createElement('tr');
        
        // Recupera il valore corrispondente dal backend usando l'indice
        // Se il valore manca, metti "0.0" o "N/D"
        const value = valuesArray[index] !== undefined ? valuesArray[index] : "0.0";

        row.innerHTML = `
            <td>${label}</td>
            <td><strong>${value}</strong></td>
        `;
        
        tableElement.appendChild(row);
    });
}

  // Pulsanti header
  document.getElementById('login-btn').addEventListener('click', showLogin)
  document.getElementById('register-btn').addEventListener('click', showRegister)

  // Login / Register
  // Modified postData to accept formId and apiPath
  function setupFormSubmission(formId, apiPath) {
    const form = document.getElementById(formId)

    if (form) { // Add null check for robustness
      form.addEventListener('submit', async (e) => {
        e.preventDefault()

        const username = document.getElementById(`${formId.replace('-form', '')}-name`).value // Extract form prefix
        const password = document.getElementById(`${formId.replace('-form', '')}-pswd`).value

        try {
          // Corrected port to 8001 and used apiPath
          const response = await fetch(`${window.API_BASE_URL}/${apiPath}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome: username, pswd: password }),
          })

          if (!response.ok) {
            const error = await response.json()
            alert(`Errore nel ${formId.replace('-form', '')}: ${error.message}`)
          } 
          const data = await response.json()

          // salva il token
          localStorage.setItem('token', data.access_token)
          showContent()
        } catch (err) {
          console.error(err)
          alert('Errore di connessione al server')
        }
      })
    } else {
      console.error(`Form with ID "${formId}" not found.`)
    }
  }

  // Call setupFormSubmission with correct form IDs and API paths
  setupFormSubmission('login-form', 'auth/login')
  setupFormSubmission('register-form', 'users/register')

  // Invio voti
  // Changed port to 8001
  document.querySelector('.content-form').addEventListener('submit', async (e) => {
    e.preventDefault()

    const votesRistorante = []
    const votesData = []

    pushVotesData(votesRistorante, 'ristorante')
    pushVotesData(votesData, 'data')

    try {
      // Corrected port to 8001
      const response = await fetch(`${window.API_BASE_URL}/votation/votation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify({ votesRistorante, votesData }),
      })

      if (response.ok) {
        alert('Voti inviati con successo!')
        document.querySelectorAll('.content-form input').forEach(i => (i.value = ''))
      } else {
        const error = await response.json()
        alert("Errore nell'invio: " + error.message)
      }
    } catch (err) {
      console.error(err)
      alert('Errore di connessione al server')
    }
  })

  document.querySelector('.show-result').addEventListener('click', async () => {
    const rawData = await fetch(`${window.API_BASE_URL}/votation/standings`, {
      method: 'GET',
      headers: {'Content-Type': 'application/json'}
    })
    const data = await rawData.json()

    // Debug part to check incoming/received data
    console.log("Dati ricevuti dal backend:", data);
    console.log("Lista Ristoranti (Averages):", data.ristoranti);
    console.log("Lista Date (Averages):", data.date);


    const lists = {
      ristoranti: ['McDonald', 'Sushi', 'Kebabbaro', 'Trattoria', 'Pizzeria'],
      date: ['19/01/2026', '20/01/2026', '21/01/2026', '22/01/2026', '26/01/2026', '27/01/2026', '28/01/2026', '29/01/2026']
    }

    const tableRistoranti = document.querySelector('.table-ristoranti')
    const tableDate = document.querySelector('.table-date')

    appendStandingsToTable(data.ristoranti, tableRistoranti, lists.ristoranti)
    appendStandingsToTable(data.date, tableDate, lists.date)


    const rawVincitori = await fetch(`${window.API_BASE_URL}/votation/final_choice`, {
      method: 'GET',
      headers: {'Content-Type': 'application/json'}
    })
    const vincitori = await rawVincitori.json()

    const indiceData = vincitori["data-vincitore"];
    const indiceRistorante = vincitori["ristorante-vincitore"];

    // Inseriamo il testo nelle classi HTML corrispondenti
    document.querySelector('.data-vincitore').textContent = lists.date[indiceData] || "N/D";
    document.querySelector('.ristorante-vincitore').textContent = lists.ristoranti[indiceRistorante] || "N/D";
  })
}); // End DOMContentLoaded
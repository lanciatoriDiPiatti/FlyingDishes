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
          const response = await fetch(`http://thecibo.velolab.cc:9001/${apiPath}`, {
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
      const response = await fetch('http://thecibo.velolab.cc/votation/yavc', {
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

}); // End DOMContentLoaded


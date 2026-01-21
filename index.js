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

// Pulsanti header
document.getElementById('login-btn').addEventListener('click', showLogin)
document.getElementById('register-btn').addEventListener('click', showRegister)

// Login / Register
function postData(formType) {
  const form = document.getElementById(`${formType}-form`)

  form.addEventListener('submit', async (e) => {
    e.preventDefault()

    const username = document.getElementById(`${formType}-name`).value
    const password = document.getElementById(`${formType}-pswd`).value

    try {
      const response = await fetch(`http://127.0.0.1:8080/${formType}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      })

      if (response.ok) {
        showContent()
      } else {
        const error = await response.json()
        alert(`Errore nel ${formType}: ${error.message}`)
      }
    } catch (err) {
      console.error(err)
      alert('Errore di connessione al server')
    }
  })
}

registerForm.hidden ? postData('login') : postData('register') 


// Invio voti
document.querySelector('.content-form').addEventListener('submit', async (e) => {
  e.preventDefault()

  const votesRistorante = []
  const votesData = []

  document.querySelectorAll('.item-row-ristorante').forEach(row => {
    const input = row.querySelector('input')

    if (input.value) {
      votesRistorante.push(parseInt(input.value))
    }
  })

  document.querySelectorAll('.item-row-data').forEach(row => {
    const input = row.querySelector('input')

    if (input.value) {
      votesData.push(parseInt(input.value))
    }
  })

  try {
    const response = await fetch('http://127.0.0.1:8080/votation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
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

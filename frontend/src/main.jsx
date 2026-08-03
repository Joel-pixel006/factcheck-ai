import { StrictMode } from 'react'
/*allows React to display things on the webpage.*/
import { createRoot } from 'react-dom/client'
/*Loads CSS styles.*/
import './index.css'
/*Imports the main App component which contains the structure and logic of the application.*/
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

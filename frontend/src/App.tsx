import { useEffect, useState } from 'react'
import { BsEyeglasses } from "react-icons/bs";
import './App.css'

function App() {
  const [items, setItems] = useState("")

  useEffect(() => {
    fetch("http://localhost:5000/url")
      .then(response => response.text())
      .then(data => setItems(data))
  }, [])

  return (
    <>
      <div>
        <a href="https://bravecareer.notion.site/Mini-Challenge-Web-Scraper-for-Visitor-Classification-12966e26414d8047a44dc41fb4ad66d2" target="_blank">
          <BsEyeglasses className="logo" size={90} />
        </a>
      </div>
      <h1>Paste a website url to see what our AI would ask</h1>
      <div className="card">
        <input name='scrape-url' placeholder='paste url here' autoFocus />
        <div>
          data returned is {items}
        </div>
      </div>
    </>
  )
}

export default App
